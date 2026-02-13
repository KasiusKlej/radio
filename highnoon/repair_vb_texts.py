import os

SRC = "original VB assets"
DST = "repaired_texts"
EXTS = (".frm", ".bas", ".log", ".mak", ".vbw")

os.makedirs(DST, exist_ok=True)

def decode_best(data):
    for enc in ("cp1250", "cp1252", "latin1"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            pass
    return None, None

for f in os.listdir(SRC):
    if f.lower().endswith(EXTS):
        src = os.path.join(SRC, f)
        dst = os.path.join(DST, f)

        with open(src, "rb") as fh:
            raw = fh.read()

        raw = raw.replace(b"\x00", b"")

        text, enc = decode_best(raw)
        if not text:
            print(f"FAILED decode: {f}")
            continue

        text = text.replace("\r\n", "\n").replace("\r", "\n")

        with open(dst, "w", encoding="utf-8") as out:
            out.write(text)

        print(f"Repaired: {f} (from {enc})")
