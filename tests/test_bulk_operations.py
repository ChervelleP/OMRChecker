import subprocess
from pathlib import Path
from PIL import Image
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Test image conversion and resizing")
    parser.add_argument("--jpg", type=str, help="Path to jpg images folder")
    parser.add_argument("--mixed", type=str, help="Path to mixed images folder")
    parser.add_argument("--png", type=str, help="Path to png images folder")
    return parser.parse_args()

def run_command(args):
    """Run main.py with args like ['-c', 'some/folder']"""
    subprocess.run(["python3", "main.py", *args], check=True)


def assert_only_pngs(folder: Path):
    """Asserts that all files in the folder (recursively) are .png"""
    for file in folder.glob("**/*"):
        if file.is_file():
            assert file.suffix.lower() == ".png", f"Found non-PNG file: {file}"


def assert_all_pngs_resized(folder: Path, size=(2480, 3508)):
    """Checks that all PNGs have the exact target size"""
    for file in folder.glob("**/*.png"):
        with Image.open(file) as img:
            assert img.size == size, f"{file} is not resized correctly. Found size: {img.size}"


if __name__ == "__main__":

    args = parse_args()
    jpg_images = Path(args.jpg) if args.jpg else None
    mixed_images = Path(args.mixed) if args.mixed else None
    png_images = Path(args.png) if args.png else None

    if jpg_images != None:
        print("\n Running convert on JPG images...")
        run_command(["-c", str(jpg_images)])
        assert_only_pngs(jpg_images)
        print(" JPG conversion: Passed")

    if mixed_images != None:
        print("\n Running convert on mixed images...")
        run_command(["-c", str(mixed_images)])
        assert_only_pngs(mixed_images)
        print(" Mixed conversion: Passed")

    if png_images != None:
        print("\n Running resize on PNG images...")
        run_command(["-r", str(png_images)])
        assert_only_pngs(png_images)
        assert_all_pngs_resized(png_images)
        print(" PNG resizing: Passed")

    print("\n ALL TESTS PASSED!\n")
