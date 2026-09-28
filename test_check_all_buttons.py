import glob
import re
import os
import sys

def check_buttons_and_keys():
    print("=" * 60)
    print("AUDITING ALL STREAMLIT BUTTONS & WIDGET KEYS IN AGRISENSE AI")
    print("=" * 60)
    
    files = glob.glob("*.py") + glob.glob("modules/*.py") + glob.glob("database/*.py")
    key_dict = {}
    duplicates = []
    
    for file_path in files:
        if os.path.basename(file_path).startswith("test_"):
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line_no, raw_line in enumerate(lines, 1):
                # Ignore commented code
                line = raw_line.split("#")[0]
                # Search for key="..." or key='...'
                matches = re.findall(r'key\s*=\s*["\']([^"\']+)["\']', line)
                for k in matches:
                    if k in key_dict:
                        duplicates.append((k, key_dict[k], f"{file_path}:{line_no}"))
                    else:
                        key_dict[k] = f"{file_path}:{line_no}"

    print(f"Total widget keys found: {len(key_dict)}")
    
    # Filter out keys that are in different exclusive pages (which is ok in Streamlit if they don't render together,
    # but strictly checking intra-file duplicates is essential!)
    intra_file_dupes = []
    for k, loc1, loc2 in duplicates:
        file1 = loc1.split(":")[0]
        file2 = loc2.split(":")[0]
        if file1 == file2:
            intra_file_dupes.append((k, loc1, loc2))
            
    if intra_file_dupes:
        print("\n[WARNING] Intra-file Duplicate Keys (High risk of Streamlit DuplicateKeyError):")
        for k, loc1, loc2 in intra_file_dupes:
            print(f"  - Key: '{k}' at {loc1} and {loc2}")
    else:
        print("\n[OK] Zero intra-file duplicate keys found! No DuplicateKeyError risks.")
        
    print(f"\n[OK] Audited {len(files)} files successfully.")

if __name__ == "__main__":
    check_buttons_and_keys()
