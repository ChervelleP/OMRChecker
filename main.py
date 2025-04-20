"""

 OMRChecker

 Author: Udayraj Deshmukh
 GitHub: https://github.com/Udayraj123

"""

import argparse
import sys
from pathlib import Path
import src.bulk_operations as bo

from src.entry import entry_point
from src.logger import logger


def parse_args():
    # construct the argument parse and parse the arguments
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-i",
        "--inputDir",
        default=["inputs"],
        # https://docs.python.org/3/library/argparse.html#nargs
        nargs="*",
        required=False,
        type=str,
        dest="input_paths",
        help="Specify an input directory.",
    )

    argparser.add_argument(
        "-d",
        "--debug",
        required=False,
        dest="debug",
        action="store_false",
        help="Enables debugging mode for showing detailed errors",
    )

    argparser.add_argument(
        "-o",
        "--outputDir",
        default="outputs",
        required=False,
        dest="output_dir",
        help="Specify an output directory.",
    )

    argparser.add_argument(
        "-a",
        "--autoAlign",
        required=False,
        dest="autoAlign",
        action="store_true",
        help="(experimental) Enables automatic template alignment - \
        use if the scans show slight misalignments.",
    )

    argparser.add_argument(
        "-l",
        "--setLayout",
        required=False,
        dest="setLayout",
        action="store_true",
        help="Set up OMR template layout - modify your json file and \
        run again until the template is set.",
    )

    argparser.add_argument(
        "-r",
        "--resize",
        required=False,
        dest="resize",
        action="store_true",
        help="Resize images before processing"
    )

    argparser.add_argument(
        "-c",
        "--convert",
        required=False,
        dest="convert",
        action="store_true",
        help="Convert from PDF or jpg to PNG "
    )

    argparser.add_argument(
        "bulk_input",
        nargs="?",
        help="Input path for conversion/resizing ",
    )


    (
        args,
        unknown,
    ) = argparser.parse_known_args()

    args = vars(args)

    if len(unknown) > 0:
        logger.warning(f"\nError: Unknown arguments: {unknown}", unknown)
        argparser.print_help()
        exit(11)
    return args


def entry_point_for_args(args):
    if args["debug"] is True:
        # Disable tracebacks
        sys.tracebacklimit = 0

    if args["convert"] or args["resize"]:
        input_path = Path(args.get("bulk_input") or "")
        if not input_path.exists():
            raise ValueError(f"Input path does not exist: {input_path}")

        if args["convert"]:
            bo.convert_to_png(input_path, input_path)  # input = output
        if args["resize"]:
            bo.resize_images(input_path, input_path)  # input = output
        return

    for root in args["input_paths"]:
        entry_point(
            Path(root),
            args,
        )


if __name__ == "__main__":
    args = parse_args()
    entry_point_for_args(args)
