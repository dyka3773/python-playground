# The file runs this way:
# `python ascii_generator.py --fname image.jpg --out output.txt --cols 80`

from PIL import Image
import numpy as np
import argparse

# Grayscale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 grayscale levels
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 grayscale levels
gscale2 = "@%#*+=-:. "

def get_average_L(img) -> np.floating:
    """Get the average brightness of a tile in the grayscale image.

    Args:
        img (PIL.Image): The image to be processed.

    Returns:
        np.floating[Image.Any]: The average brightness of the tile.
    """
    img = np.array(img)
    w, h = img.shape
    return np.average(img.reshape(w*h))

def generate_ascii_img(image: Image.Image, rows: int, tile_width: int, tile_height: int, height: int, width: int) -> list[str]:
    """Generate the ASCII art image from the original image.
    
    Args:
        image (PIL.Image): The original image to be processed.
        rows (int): The number of rows in the ASCII art image.
        tile_width (int): The width of each tile in the ASCII art image.
        tile_height (int): The height of each tile in the ASCII art image.
        height (int): The height of the original image.
        width (int): The width of the original image.
        
    Returns:
        list[str]: A list of strings representing the ASCII art image.
    """
    ascii_img: list[str] = []
    # Generate the list of tile dimensions
    for r in range(rows):
        #  Calculate the starting and ending y-coordinates of each image tile
        y1 = int(r*tile_height)
        y2 = int((r+1)*tile_height)
        if r == rows-1:
            y2 = height
        ascii_img.append("")
        for c in range(COLS):
            # Calculate the starting and ending x-coordinates of each image tile
            x1 = int(c*tile_width)
            x2 = int((c+1)*tile_width)
            if c == COLS-1:
                x2 = width
            
            # Crop the image to extract the tile into another Image object
            img: Image.Image = image.crop((x1, y1, x2, y2))
            # Get the average brightness of the tile
            avg = int(get_average_L(img))
            # Use the average brightness to determine the character to use
            if HIGH_G_RES:
                gsval = gscale1[int((avg/255)*(len(gscale1)-1))]
            else:
                gsval = gscale2[int((avg/255)*(len(gscale2)-1))]
            ascii_img[r] += gsval

    return ascii_img

def main():
    # Define command line options for the program
    parser = argparse.ArgumentParser(description='Generate an ASCII art image from an image.')
    parser.add_argument('--fname', dest='FILENAME', help='The name of the image file to be converted to ASCII art.', required=True)
    parser.add_argument('--out', dest='OUTPUT_FILE', help='The name of the output file.', required=True)
    parser.add_argument('--cols', dest='COLS', help='The number of columns in the image.', required=False)
    parser.add_argument('--font_scale', dest='FONT_SCALE', help='The font scale to use.', required=False)
    parser.add_argument('--res', dest='HIGH_G_RES', help='Whether to use a high-resolution font.', required=False, action='store_false')
    args = parser.parse_args()

    # Set the global variables
    global FILENAME, OUTPUT_FILE, COLS, FONT_SCALE, HIGH_G_RES

    # Setting up the hyperparameters
    FILENAME = args.FILENAME
    OUTPUT_FILE = args.OUTPUT_FILE
    COLS = int(args.COLS) if args.COLS else 80 # Number of columns in the image will be 80 by default
    FONT_SCALE = int(args.FONT_SCALE) if args.FONT_SCALE else 0.43 # Font scale will be 0.43 by default (0.43 is the default font scale for the Courier font)
    HIGH_G_RES = False if args.HIGH_G_RES else True # If the user doesn't want to use a high-resolution font, set this to False

    # Open the image file and convert it to grayscale
    image: Image.Image = Image.open(FILENAME).convert('L') #  The "L" stands for luminance
    # Image dims
    width, height = image.size[0], image.size[1]
    # Setting up tile size
    tile_width = int(width / COLS)
    tile_height = int(tile_width/FONT_SCALE)
    # Compute the number of rows to use in the final grid
    rows = int(height / tile_height)

    print("input image dims: %d x %d" % (width, height))
    print("cols: %d, rows: %d" % (COLS, rows))
    print("tile dims: %d x %d" % (tile_width, tile_height))

    # Check if image size is too small
    if COLS > width or rows > height:
        print("Image too small for specified cols!")
        exit(1)

    print("Generating ASCII art...")

    # Write the ASCII art to a file
    with open(OUTPUT_FILE, 'w') as f:
        ascii_img: list[str] = generate_ascii_img(image,rows,tile_width,tile_height, height, width)
        for row in ascii_img:
            f.write(row + '\n')
    print("ASCII art generated!")
    print("ASCII art written to %s" % OUTPUT_FILE)


if __name__ == '__main__':
    main()