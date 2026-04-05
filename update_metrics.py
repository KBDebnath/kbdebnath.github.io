import re
import requests
from scholarly import scholarly

# --- SETTINGS ---
FILE_PATH = "publications.html"
GS_ID = "fr35XxAAAAAJ" # Your Google Scholar ID

def get_stats():
    # 1. Google Scholar via Scholarly (No browser needed)
    author = scholarly.search_author_id(GS_ID)
    scholarly.fill(author, sections=['indices'])
    
    return {
        "gs_cite": author.get('citedby', 0),
        "gs_h": author.get('hindex', 0),
        "gs_i10": author.get('i10index', 0)
    }

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
