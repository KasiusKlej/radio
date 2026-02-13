import os

# === Project-specific configuration ===
SRC_DIR = "original_VB_assets"
DST_DIR = "extracted_vb_source"
os.makedirs(DST_DIR, exist_ok=True)

# File types
TEXT_EXTS = (".bas", ".frm", ".log", ".mak")
SKIP_EXTS = (".vbw",)  # Pure binary workspace files

# VB keywords to help detect text blocks in FRM/BAS
VB_KEYWORDS = (
    "VERSION", "Attribute", "Option", "Begin", "End",
    "Private", "Public", "Sub", "Function", "Dim", "'"
)

def is_vb_line(line):
    """Return True if the line contains likely VB code or text."""
    stripped = line.strip()
    if not stripped:
        return False
    # Check if line starts with VB keyword OR has printable content
    return any(stripped.startswith(k) for k in VB_KEYWORDS) or any(c.isprintable() for c in stripped)

def process_file(src_path, dst_path):
    """Extract VB text from FRM/BAS or copy MAK files."""
    ext = os.path.splitext(src_path)[1].lower()

    if ext in SKIP_EXTS:
        print(f"Skipping binary file: {src_path}")
        return

    try:
        with open(src_path, "rb") as f:
            raw = f.read()

        # Remove only NUL bytes (true binary poison)
        raw = raw.replace(b"\x00", b"")

        # Decode bytes safely (latin1 preserves legacy VB bytes)
        text = raw.decode("latin1", errors="ignore")
        lines = text.splitlines()

        output_lines = []

        # For FRM/BAS: keep all lines that look like VB
        for line in lines:
            if is_vb_line(line):
                output_lines.append(line.rstrip())

        if output_lines or ext == ".mak":
            # Make output path directory if needed
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            with open(dst_path, "w", encoding="utf-8") as out:
                out.write("\n".join(output_lines) if output_lines else text)
            print(f"Extracted: {os.path.relpath(dst_path, DST_DIR)}")
        else:
            print(f"No VB source found (skipped): {os.path.relpath(src_path, SRC_DIR)}")

    except Exception as e:
        print(f"FAILED: {src_path} ({e})")

# Process files only in the top level of original_VB_assets (no recursion)
for fname in sorted(os.listdir(SRC_DIR)):
    src_file = os.path.join(SRC_DIR, fname)
    if not os.path.isfile(src_file):
        continue

    dst_file = os.path.join(DST_DIR, fname)
    process_file(src_file, dst_file)