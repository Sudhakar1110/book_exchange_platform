import os
import json
import shutil

base_dir = r"c:\Users\sujai\Downloads\git\book_exchange_platform\book_exchange_platform-main\book_exchange"
target_doctype_dir = os.path.join(base_dir, "book_exchange_platform", "doctype")

# Ensure target directory exists
os.makedirs(target_doctype_dir, exist_ok=True)
if not os.path.exists(os.path.join(target_doctype_dir, "__init__.py")):
    with open(os.path.join(target_doctype_dir, "__init__.py"), "w") as f:
        pass

modules_to_move = [
    "book_management",
    "user_management",
    "exchange_management",
    "donation_management"
]

for mod in modules_to_move:
    doctype_dir = os.path.join(base_dir, mod, "doctype")
    if os.path.exists(doctype_dir):
        for dt_folder in os.listdir(doctype_dir):
            src = os.path.join(doctype_dir, dt_folder)
            if os.path.isdir(src):
                dest = os.path.join(target_doctype_dir, dt_folder)
                
                # Move directory
                if not os.path.exists(dest):
                    shutil.move(src, dest)
                else:
                    print(f"Destination {dest} already exists.")
                    
                # Update JSON file
                json_file = os.path.join(dest, f"{dt_folder}.json")
                if os.path.exists(json_file):
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    data["module"] = "Book Exchange Platform"
                    
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=1)

# Remove old modules from modules.txt
modules_txt_path = os.path.join(base_dir, "modules.txt")
if os.path.exists(modules_txt_path):
    with open(modules_txt_path, "w", encoding="utf-8") as f:
        f.write("Book Exchange Platform\n")

print("Moved DocTypes and updated JSONs successfully.")
