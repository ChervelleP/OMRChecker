import subprocess
from pathlib import Path
from PIL import Image


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
    # Set up paths
    base_path = Path.home() / "Desktop/img_test"
    jpg_images = base_path / "jpg_images"
    mixed_images = base_path / "mixed_images"
    png_images = base_path / "png_images"

    print("\n Running convert on JPG images...")
    run_command(["-c", str(jpg_images)])
    assert_only_pngs(jpg_images)
    print(" JPG conversion: Passed")

    print("\n Running convert on mixed images...")
    run_command(["-c", str(mixed_images)])
    assert_only_pngs(mixed_images)
    print(" Mixed conversion: Passed")

    print("\n Running resize on PNG images...")
    run_command(["-r", str(png_images)])
    assert_only_pngs(png_images)
    assert_all_pngs_resized(png_images)
    print(" PNG resizing: Passed")

    print("\n ALL TESTS PASSED!\n")
