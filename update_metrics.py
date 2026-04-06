import re
import json

HTML_FILE = "publications.html"
DATA_FILE = "metrics.json"

def update_website():
    # 1. Load your manually updated numbers
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # 2. Read the publications page
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 3. Use Regex to find the numbers and swap them
    # Update Google Scholar Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\))', 
                  rf'\1{data["gs_cite"]}\2', html)
    
    # Update Scopus Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Scopus \[S\]\))', 
                  rf'\1{data["scopus_cite"]}\2', html)

    # Update Web of Science Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Web of Science \[WoS\]\))', 
                  rf'\1{data["wos_cite"]}\2', html)

    # Update h-index (Handles the GS/S/WoS format)
    h_combined = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'(<span class="metric-value">)\d+ / \d+ / \d+(</span><span class="metric-label">h-index)', 
                  rf'\1{h_combined}\2', html)

    # Update i10-index
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">i10-index<br>\(GS\))', 
                  rf'\1{data["gs_i10"]}\2', html)

    # 4. Save changes
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Success: publications.html updated.")

if __name__ == "__main__":
    update_website()
