import argparse
import os, errno
import random
import string

from tqdm import tqdm
from string_generator import create_strings_from_dict
from data_generator import generate
from multiprocessing import Pool
from utils import *


def valid_range(s):
    if len(s.split(',')) > 2:
        raise argparse.ArgumentError("The given range is invalid, please use ?,? format.")
    return tuple([int(i) for i in s.split(',')])

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(description='Generate synthetic text data for text recognition.')
    parser.add_argument(
        "--output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        default="out/",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be fr (French), en (English), es (Spanish), de (German), or cn (Chinese).",
        default="en"
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",
        help="The number of images to be created. default >20",
        default=1000
    )
    parser.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",
        help="Define how many words should be included in each generated sample. If the text source is Wikipedia, this is the MINIMUM length",
        default=1
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=False
    )
    parser.add_argument(
        "-f",
        "--format",
        type=int,
        nargs="?",
        help="Define the height of the produced images if horizontal, else the width",
        default=32,
    )
#     parser.add_argument(
#         "-t",
#         "--thread_count",
#         type=int,
#         nargs="?",
#         help="Define the number of thread to use for image generation",
#         default=1,
#     )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="jpg",
    )
    parser.add_argument(
        "-fs",
        "--font_size",
        type=int,
        nargs="?",
        help="Define the font size",
        default=1,
    )
    parser.add_argument(
        "-b",
        "--background_dir",
        type=str,
        nargs="?",
        help="Define background dir",
        default='./background',
    )
    parser.add_argument(
        "-wd",
        "--width",
        type=int,
        nargs="?",
        help="Define the width of the resulting image. If not set it will be the width of the text + 10. If the width of the generated text is bigger that number will be used",
        default=-1
    )
    parser.add_argument(
        "-or",
        "--orientation",
        type=int,
        nargs="?",
        help="Define the orientation of the text. 0: Horizontal, 1: Vertical",
        default=0
    )
    parser.add_argument(
        "-tc",
        "--text_color",
        type=str,
        nargs="?",
        help="Define the text's color, should be either a single hex color or a range in the ?,? format.",
        default='#282828'
    )
    parser.add_argument(
        "-sw",
        "--space_width",
        type=float,
        nargs="?",
        help="Define the width of the spaces between words. 2.0 means twice the normal space width",
        default=1.0
    )

    return parser.parse_args()


def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = parse_arguments()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    lang_dict = load_dict(args.language)

    # Create font (path) list
    fonts = load_fonts(args.language)

    # Creating synthetic sentences (or word)
    strings = []
    strings = create_strings_from_dict(args.length, args.random, args.count, lang_dict)
    string_count = len(strings)
    
    imgLists = load_img(args.background_dir)
    
    for i,img in enumerate(imgLists):
        try:
            generate(i,img,
                   random.sample(strings,random.randint(1,40)),
                   fonts[random.randrange(0,len(fonts))],
                   args.output_dir,args.extension,args.width,args.text_color,
                   args.orientation,args.space_width,args.font_size)
        except:
            continue

if __name__ == '__main__':
        main()
