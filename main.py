from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import time
import sys
import argparse

parser = argparse.ArgumentParser(description='Convert CT to Xray')
parser.add_argument('CT_dir', type=str, help='Name of the directory containing the CT volume')
parser.add_argument('mask_dir', type=str, help='Name of the directory containing the masks')

args = parser.parse_args()

def sort_list(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

def create_image(dirname, dirname2, label):
    if dirname[-1] == "/":
        dirname = dirname[:-1]
    images = glob.glob(str(dirname) + "/*.png")

    if dirname2[-1] == "/":
        dirname2 = dirname2[:-1]
    images2 = glob.glob(str(dirname2) + "/*.png")

    # Sort images alphanumerically by filename to ensure that z loops from front to back
    images = sort_list(images)
    images2 = sort_list(images2)

    p = np.zeros((len(images), Image.open(images[0]).convert('L').size[0]))

    # setup toolbar
    toolbar_width = int(len(images)/5 + 1)
    sys.stdout.write(label + " [%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))

    # Loop through CT slices from front to back
    for z in range(len(images)):
        img = Image.open(images[z]).convert('L')  # convert image to 8-bit grayscale
        HEIGHT, WIDTH = img.size
        data = list(img.getdata()) # convert image data to a list of integers
        # convert that to 2D list (list of lists of integers)
        pixels = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

        img2 = Image.open(images2[z]).convert('L') 
        data2 = list(img2.getdata()) 
        pixels2 = [data2[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

        for r in range(HEIGHT):
            for c in range(WIDTH):
                if pixels2[r][c] != 0:
                    pixels[r][c] = pixels2[r][c]

        # Loop from left to right on the CT slice
        for x in range(WIDTH):
            # Sum y values in the current x column
            sum = 0
            for y in range(HEIGHT):
                sum += pixels[y][x]
            # Assign sum to the point (x, z) on the coronal image - p[z][x] in the pixel array, 
            # since z represents height (rows) and x represents length (columns)
            p[len(images) - 1 - z][x] = sum

        if z % 5 == 0:
            # update the bar
            sys.stdout.write("-")
            sys.stdout.flush()
    sys.stdout.write("]\n")

    plt.imshow(p, cmap='gray')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig('xray.png', bbox_inches = 'tight',
        pad_inches = 0)

# Save and display image
create_image(args.CT_dir, args.mask_dir, "Creating X-ray:")

final_img = Image.open('xray.png')
size = 300
if final_img.size[1] < 300:
    final_img = final_img.resize((final_img.size[0], 300))    

final_img.save('xray.png')
print('Xray saved to \'xray.png\'')
final_img.show()