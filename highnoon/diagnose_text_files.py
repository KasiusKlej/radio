import os

ROOT = "original VB assets"
TEXT_EXT = (".frm", ".bas", ".log", ".mak", ".vbw")

def analyze(path):
    with open(path, "rb") as f:
        data = f.read()

    nul_count = data.count(b"\x00")

    # Try decoding with common legacy encodings
    encodings = ["utf-8", "cp1250", "cp1252", "latin1"]
    results = {}

    for enc in encodings:
        try:
            data.decode(enc)
            results[enc] = "OK"
        except UnicodeDecodeError:
            results[enc] = "FAIL"

    return nul_count, results

for root, _, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(TEXT_EXT):
            path = os.path.join(root, f)
            nul_count, results = analyze(path)
            print(f"\n{path}")
            print(f"  NUL bytes: {nul_count}")
            for enc, status in results.items():
                print(f"  {enc:8}: {status}")
