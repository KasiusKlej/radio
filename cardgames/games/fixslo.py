# fix_mojibake.py
def repair_encoding(filename):
    try:
        # Read the corrupted file as "Latin-1" (which preserves the raw bytes)
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # This reverses the "UTF-8 viewed as CP1250" error
        # We encode back to raw bytes then decode properly
        repaired = content.encode('latin-1').decode('cp1250')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(repaired)
        print(f"Fixed {filename}")
    except:
        print(f"Could not fix {filename}. Use backup.")

repair_encoding('slo.txt')
repair_encoding('yu.txt')