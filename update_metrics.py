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

    # We use very specific 'Anchors' to ensure GS data stays in GS and WoS in WoS
    
    # 1. Update Google Scholar [GS]
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\))', 
                  rf'\g<1>{data["gs_cite"]}\g<2>', html)
    
    # 2. Update Scopus [S]
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Scopus \[S\]\))', 
                  rf'\g<1>{data["scopus_cite"]}\g<2>', html)

    # 3. Update Web of Science [WoS]
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Web of Science \[WoS\]\))', 
                  rf'\g<1>{data["wos_cite"]}\g<2>', html)

    # 4. Update h-index (GS / S / WoS)
    h_str = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">h-index<br>\(GS/S/WoS\))', 
                  rf'\g<1>{h_str}\g<2>', html)

    # 5. Update i10-index
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">i10-index<br>\(GS\))', 
                  rf'\g<1>{data["gs_i10"]}\g<2>', html)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Success: Updated GS to {data['gs_cite']} and WoS to {data['wos_cite']}.")

if __name__ == "__main__":
    update_website()
