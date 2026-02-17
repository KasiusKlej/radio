# resize_cards.py
from PIL import Image
import os

source_dir = "static/cards/"
target_size = (89, 132) # Faithful to your original design

for filename in os.listdir(source_dir):
    if filename.endswith(".bmp"):
        img = Image.open(os.path.join(source_dir, filename))
        # Use Image.LANCZOS for older Pillow versions, or Image.ANTIALIAS for very old ones
        try:
            resample_filter = Image.LANCZOS
        except AttributeError:
            resample_filter = Image.ANTIALIAS
            
        img = img.resize(target_size, resample=resample_filter)
        new_name = filename.replace(".bmp", ".png")
        img.save(os.path.join(source_dir, new_name), "PNG")
        print(f"Successfully converted {filename} to {new_name}")