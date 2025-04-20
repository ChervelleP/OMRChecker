from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
import warnings


def convert_to_png(input_path: Path, output_path: Path):
    image_extensions = {".jpg", ".jpeg", ".pdf", ".png"}

    for file in input_path.glob("**/*"):
        if file.suffix.lower() not in image_extensions:
            warnings.warn(f"File '{file.name}' can't be converted – unsupported format.")
            continue

        if file.suffix.lower() == ".pdf":
            try:
                pages = convert_from_path(file, dpi=300)
                for idx, page in enumerate(pages):
                    png_name = file.stem + f"_page{idx+1}.png"
                    save_path = output_path / png_name
                    page.save(save_path, "PNG")

                if input_path == output_path:
                    file.unlink()
            except Exception as e:
                print(f"Error converting PDF {file}: {e}")

        elif file.suffix.lower() in {".jpg", ".jpeg"}:
            try:
                with Image.open(file) as img:
                    png_name = file.stem + ".png"
                    save_path = output_path / png_name
                    img.convert("RGB").save(save_path, "PNG")

                if input_path == output_path:
                    file.unlink()
            except Exception as e:
                print(f"Error converting JPG {file}: {e}")

def resize_images(input_path: Path, output_path: Path, size=(2480, 3508)):
    """
    Resizes all PNG images in input_path to a specified size (default A4 at 300 DPI).
    Overwrites in-place if input_path == output_path.
    """

    for file in input_path.glob("**/*.png"):
        try:
            with Image.open(file) as img:
                resized = img.resize(size, Image.LANCZOS)
                save_path = output_path / file.name
                resized.save(save_path)
        except Exception as e:
            print(f"Error resizing {file}: {e}")
