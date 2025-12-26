#!/usr/bin/env python3
"""
Batch Image Resizer Tool

Resizes and adjusts quality of JPEG images in a directory.

Arguments:
    --input, -i: Input directory containing JPEGs
    --output, -o: Output directory (default: input_dir/resized)
    --width: Max width (maintains aspect ratio if height not set)
    --height: Max height (maintains aspect ratio if width not set)
    --quality, -q: JPEG quality (1-100, default: 85)

Example:
    python3 scripts/image_resizer/resizer.py -i ./photos --width 1920 --quality 80
"""
import sys
import argparse
import logging
from pathlib import Path
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def setup_args():
    parser = argparse.ArgumentParser(description="Batch Resize & Compress JPEG Images")
    parser.add_argument("--input", "-i", type=Path, required=True, help="Input directory containing images")
    parser.add_argument("--output", "-o", type=Path, help="Output directory (default: input/resized)")
    parser.add_argument("--width", type=int, help="Target maximum width")
    parser.add_argument("--height", type=int, help="Target maximum height")
    parser.add_argument("--quality", "-q", type=int, default=85, help="JPEG Quality (1-100)")
    return parser.parse_args()

def process_image(file_path: Path, output_dir: Path, width: int, height: int, quality: int):
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary (e.g. if RGBA)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            target_width = width
            target_height = height

            # Calculate new dimensions while maintaining aspect ratio
            if width and height:
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            elif width:
                w_percent = (width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                img = img.resize((width, h_size), Image.Resampling.LANCZOS)
            elif height:
                h_percent = (height / float(img.size[1]))
                w_size = int((float(img.size[0]) * float(h_percent)))
                img = img.resize((w_size, height), Image.Resampling.LANCZOS)
            
            # If neither width nor height is specified, keep original dimensions but apply quality compression.
            
            output_file = output_dir / file_path.name
            img.save(output_file, "JPEG", quality=quality)
            logging.info(f"✅ Processed: {file_path.name} -> {output_file} (Quality: {quality})")
            
    except Exception as e:
        logging.error(f"❌ Failed to process {file_path.name}: {e}")

def main():
    args = setup_args()

    if not args.input.exists():
        logging.error(f"❌ Input directory not found: {args.input}")
        sys.exit(1)

    output_dir = args.output if args.output else args.input / "resized"
    output_dir.mkdir(parents=True, exist_ok=True)

    images = list(args.input.glob("*.jpg")) + list(args.input.glob("*.jpeg")) + list(args.input.glob("*.JPG")) + list(args.input.glob("*.JPEG"))
    
    if not images:
        logging.warning(f"⚠️ No JPEG images found in {args.input}")
        sys.exit(0)

    logging.info(f"🚀 Found {len(images)} images. Starting processing...")
    logging.info(f"📂 Output Directory: {output_dir}")
    
    for img_path in images:
        process_image(img_path, output_dir, args.width, args.height, args.quality)

    logging.info("🎉 Batch processing complete.")

if __name__ == "__main__":
    main()
