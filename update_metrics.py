import re
import json
import os

HTML_FILE = "publications.html"
DATA_FILE = "metrics.json"

def update_website():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # This new logic looks for the LABEL first, then finds the closest number before it.
    # It is much more reliable than matching the whole line.
    
    # 1. Update GS Citations
    html = re.sub(r'<span class="metric-value">(\d+)</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\)', 
                  f'<span class="metric-value">{data["gs_cite"]}</span><span class="metric-label">Citations<br>(Google Scholar [GS])', html)
    
    # 2. Update Scopus Citations
    html = re.sub(r'<span class="metric-value">(\d+)</span><span class="metric-label">Citations<br>\(Scopus \[S\]\)', 
                  f'<span class="metric-value">{data["scopus_cite"]}</span><span class="metric-label">Citations<br>(Scopus [S])', html)

    # 3. Update WoS Citations
    html = re.sub(r'<span class="metric-value">(\d+)</span><span class="metric-label">Citations<br>\(Web of Science \[WoS\]\)', 
                  f'<span class="metric-value">{data["wos_cite"]}</span><span class="metric-label">Citations<br>(Web of Science [WoS])', html)

    # 4. Update h-index (GS / S / WoS)
    h_str = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'<span class="metric-value">(\d+ / \d+ / \d+)</span><span class="metric-label">h-index', 
                  f'<span class="metric-value">{h_str}</span><span class="metric-label">h-index', html)

    # 5. Update i10-index
    html = re.sub(r'<span class="metric-value">(\d+)</span><span class="metric-label">i10-index<br>\(GS\)', 
                  f'<span class="metric-value">{data["gs_i10"]}</span><span class="metric-label">i10-index<br>(GS)', html)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Metrics injection complete.")

if __name__ == "__main__":
    update_website()
