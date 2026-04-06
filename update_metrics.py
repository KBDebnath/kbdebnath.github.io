import re
import json
import os

HTML_FILE = "publications.html"
DATA_FILE = "metrics.json"

def update_website():
    if not os.path.exists(DATA_FILE) or not os.path.exists(HTML_FILE):
        print("Error: Files not found.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # This regex is much 'looser' - it finds the number inside the span 
    # regardless of small spaces or formatting in the label following it.
    
    # 1. GS Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations.*?Google Scholar)', 
                  rf'\g<1>{data["gs_cite"]}\g<2>', html, flags=re.DOTALL)
    
    # 2. Scopus Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations.*?Scopus)', 
                  rf'\g<1>{data["scopus_cite"]}\g<2>', html, flags=re.DOTALL)

    # 3. WoS Citations
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations.*?Web of Science)', 
                  rf'\g<1>{data["wos_cite"]}\g<2>', html, flags=re.DOTALL)

    # 4. h-index (Handles the GS/S/WoS format)
    h_str = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'(<span class="metric-value">)[\d\s/]+(</span><span class="metric-label">h-index)', 
                  rf'\g<1>{h_str}\g<2>', html, flags=re.DOTALL)

    # 5. i10-index
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">i10-index)', 
                  rf'\g<1>{data["gs_i10"]}\g<2>', html, flags=re.DOTALL)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Success: Metrics updated.")

if __name__ == "__main__":
    update_website()
