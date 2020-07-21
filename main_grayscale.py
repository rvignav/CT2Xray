from PIL import Image
import numpy as np
import glob
import re
import time
import sys
import cv2

images = glob.glob("CT/*.png")

def sort_list( l ):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

# Sort images alphanumerically by filename to ensure that z loops from front to back
images = sort_list(images)

p = np.zeros((len(images), Image.open(images[0]).convert('L').size[0]))

# setup toolbar
toolbar_width = int(len(images)/5)
sys.stdout.write("Progress: [%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

# Loop through CT slices from front to back
for z in range(len(images)):
    img = Image.open(images[z]).convert('L')  # convert image to 8-bit grayscale
    HEIGHT, WIDTH = img.size
    data = list(img.getdata()) # convert image data to a list of integers
    # convert that to 2D list (list of lists of integers)
    pixels = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    # Loop from left to right on the CT slice
    for x in range(WIDTH):
        # Sum y values in the current x column
        sum = 0
        for y in range(HEIGHT):
            sum += pixels[y][x]
        # Assign sum to the point (x, z) on the coronal image - p[z][x] in the pixel array, 
        # since z represents height (rows) and x represents length (columns)
        p[len(images) - 1 - z][x] = sum / HEIGHT
    if z % 5 == 0:
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

sys.stdout.write("]\n")
            
# Save and display image
array = np.array(p, dtype=np.uint8)
xray = Image.fromarray(np.uint8(array * 255) , 'L')
xray.save('xray.png')
print('Xray saved to \'xray.png\'')
xray.show()