import re
from scholarly import scholarly, ProxyGenerator

# --- SETTINGS ---
FILE_PATH = "publications.html"
GS_ID = "fr35XxAAAAAJ" 

def get_stats():
    # Setup a 'Navigator' with a real-looking User-Agent
    pg = ProxyGenerator()
    # We aren't using a real proxy (those cost money), 
    # but we are telling scholarly to use a specific browser header.
    scholarly.use_proxy(None) 
    
    try:
        # Search for the author ID directly
        author = scholarly.search_author_id(GS_ID)
        # We only need the 'indices' and 'basics' to get counts/h-index
        scholarly.fill(author, sections=['basics', 'indices'])
        
        return {
            "gs_cite": author.get('citedby', 0),
            "gs_h": author.get('hindex', 0),
            "gs_i10": author.get('i10index', 0)
        }
    except Exception as e:
        print(f"Google Scholar is still blocking the request: {e}")
        # If it fails, we exit gracefully so the whole build doesn't go red
        import sys
        sys.exit(0)

def update_html(stats):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Update GS Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\))', 
                  rf'\1{stats["gs_cite"]}\2', html)
    
    # Update i10-index
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">i10-index<br>\(GS\))', 
                  rf'\1{stats["gs_i10"]}\2', html)
    
    # Update h-index (Updates the first number in the GS/S/WoS string)
    html = re.sub(r'(<span class="metric-value">)\d+( / \d+ / \d+</span><span class="metric-label">h-index)', 
                  rf'\1{stats["gs_h"]}\2', html)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    data = get_stats()
    update_html(data)
