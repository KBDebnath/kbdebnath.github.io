import re
import json
import os

HTML_FILE = "publications.html"
DATA_FILE = "metrics.json"

def update_website():
    # Check if files exist to avoid Exit Code 1
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found in root directory.")
        return
    if not os.path.exists(HTML_FILE):
        print(f"Error: {HTML_FILE} not found in root directory.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Updated Regex to be more flexible with whitespace
    # GS Citations
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\))', 
                  rf'\1{data["gs_cite"]}\2', html)
    
    # Scopus Citations
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Scopus \[S\]\))', 
                  rf'\1{data["scopus_cite"]}\2', html)

    # WoS Citations
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Web of Science \[WoS\]\))', 
                  rf'\1{data["wos_cite"]}\2', html)

    # h-index (matches any combination of numbers/slashes)
    h_combined = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">h-index)', 
                  rf'\1{h_combined}\2', html)

    # i10-index
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">i10-index<br>\(GS\))', 
                  rf'\1{data["gs_i10"]}\2', html)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully synchronized HTML with JSON data.")

if __name__ == "__main__":
    update_website()
