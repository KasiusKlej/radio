import os
import mimetypes

ROOT = "."

TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))

def is_text_file(path, blocksize=512):
    try:
        with open(path, "rb") as f:
            chunk = f.read(blocksize)
        return not bool(chunk.translate(None, TEXT_CHARS))
    except Exception:
        return False

def magic_bytes(path, n=8):
    try:
        with open(path, "rb") as f:
            return f.read(n)
    except Exception:
        return b""

print(f"{'FILE':60} {'SIZE':>8} {'TYPE':10} {'MIME':25} MAGIC")
print("-" * 120)

for root, _, files in os.walk(ROOT):
    for name in files:
        path = os.path.join(root, name)
        size = os.path.getsize(path)
        mime, _ = mimetypes.guess_type(path)
        kind = "TEXT" if is_text_file(path) else "BINARY"
        magic = magic_bytes(path).hex(" ")
        print(f"{path:60} {size:8} {kind:10} {str(mime):25} {magic}")