import os
from PIL import Image

# Configuration
INPUT_DIR = "assets/img"  # Folder with original JPG/PNGs
OUTPUT_DIR = "assets/img"                # Jekyll's target folder
TARGET_SIZES = [800, 1400]              # Widths to generate
QUALITY = 80                            # WebP quality (0-100)

def convert_to_webp():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process all JPG/PNG files in input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(INPUT_DIR, filename)
            base_name = os.path.splitext(filename)[0]  # Remove extension
            
            with Image.open(input_path) as img:
                for width in TARGET_SIZES:
                    # Resize image (maintain aspect ratio)
                    w_percent = width / float(img.size[0])
                    height = int(float(img.size[1]) * float(w_percent))
                    resized_img = img.resize((width, height), Image.LANCZOS)
                    
                    # Save as WebP
                    output_name = f"{base_name}-{width}.webp"
                    output_path = os.path.join(OUTPUT_DIR, output_name)
                    resized_img.save(output_path, "webp", quality=QUALITY)
                    print(f"Saved: {output_path}")

if __name__ == "__main__":
    convert_to_webp()
    print("Conversion complete!")