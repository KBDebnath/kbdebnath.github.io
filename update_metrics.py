import re
import json
import os

HTML_FILE = "publications.html"
DATA_FILE = "metrics.json"

def update_website():
    if not os.path.exists(DATA_FILE) or not os.path.exists(HTML_FILE):
        print("Missing files. Ensure both metrics.json and publications.html exist.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Safe regex updates using named groups to avoid "invalid group reference"
    patterns = {
        r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\))': data["gs_cite"],
        r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Scopus \[S\]\))': data["scopus_cite"],
        r'(<span class="metric-value">).*?(</span><span class="metric-label">Citations<br>\(Web of Science \[WoS\]\))': data["wos_cite"],
        r'(<span class="metric-value">).*?(</span><span class="metric-label">i10-index<br>\(GS\))': data["gs_i10"]
    }

    for pattern, val in patterns.items():
        html = re.sub(pattern, rf'\g<1>{val}\g<2>', html)

    # Special case for combined h-index string
    h_str = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'(<span class="metric-value">).*?(</span><span class="metric-label">h-index)', rf'\g<1>{h_str}\g<2>', html)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully synchronized metrics.")

if __name__ == "__main__":
    update_website()
