import re
import json

# --- SETTINGS ---
HTML_FILE = "publications.html"
DATA_FILE = "metrics.json"

def update_website():
    # 1. Read the numbers from your JSON file
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # 2. Read your HTML file
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 3. Use Regex to swap the numbers in the HTML
    # Update Citations GS
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Google Scholar \[GS\]\))', 
                  rf'\1{data["gs_cite"]}\2', html)
    
    # Update Citations Scopus
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Scopus \[S\]\))', 
                  rf'\1{data["scopus_cite"]}\2', html)

    # Update Citations WoS
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">Citations<br>\(Web of Science \[WoS\]\))', 
                  rf'\1{data["wos_cite"]}\2', html)

    # Update h-index (GS / S / WoS)
    new_h_string = f'{data["gs_h"]} / {data["scopus_h"]} / {data["wos_h"]}'
    html = re.sub(r'(<span class="metric-value">)\d+ / \d+ / \d+(</span><span class="metric-label">h-index)', 
                  rf'\1{new_h_string}\2', html)

    # Update i10-index
    html = re.sub(r'(<span class="metric-value">)\d+(</span><span class="metric-label">i10-index<br>\(GS\))', 
                  rf'\1{data["gs_i10"]}\2', html)

    # 4. Save the updated HTML
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Success: publications.html updated with latest metrics.")

if __name__ == "__main__":
    update_website()
