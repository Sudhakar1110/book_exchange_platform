import json
import os

base_dir = r"c:\Users\sujai\Downloads\git\book_exchange_platform\book_exchange_platform-main\book_exchange\book_exchange_platform\workspace"

reports_ws = os.path.join(base_dir, "reports", "reports.json")
main_ws = os.path.join(base_dir, "book_exchange_platform", "book_exchange_platform.json")

def update_ws(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Check if report already exists in links
    exists = any(l.get("link_to") == "Member Activity Report" for l in data.get("links", []))
    if exists:
        return
        
    data["links"].append({
        "hidden": 0,
        "is_query_report": 1,
        "label": "Member Activity Report",
        "link_count": 0,
        "link_to": "Member Activity Report",
        "link_type": "Report",
        "onboard": 0,
        "type": "Link"
    })
    
    data["shortcuts"].append({
        "color": "Gray",
        "doc_view": "",
        "label": "Member Activity Report",
        "link_to": "Member Activity Report",
        "type": "Report"
    })
    
    # Add to content
    content = json.loads(data["content"])
    content.append({
        "id": "member_activity_report",
        "type": "shortcut",
        "data": {
            "shortcut_name": "Member Activity Report",
            "col": 3
        }
    })
    data["content"] = json.dumps(content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)

update_ws(reports_ws)
update_ws(main_ws)
print("Workspaces updated successfully.")
