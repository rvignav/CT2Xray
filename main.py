from PIL import Image
import numpy as np
import glob
import re
import time
import sys

images = glob.glob("CT/*.png")

def sort_list( l ):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

# Sort images alphanumerically by filename to ensure that z loops from front to back
images = sort_list(images)

# Handle images of different sizes
m = np.asarray(Image.open(images[0])).shape[1]
for i in range(len(images)):
    m = max(m, np.asarray(Image.open(images[i])).shape[1])
p = np.zeros((len(images), m, 3))

toolbar_width = int(len(images)/5)

# setup toolbar
sys.stdout.write("Progress: [%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

# Loop through CT slices from front to back
for z in range(len(images)):
    image = Image.open(images[z])
    pixels = np.asarray(image)
    if len(pixels.shape) == 2:	
        # Loop from left to right on the CT slice
        for x in range(pixels.shape[1]):
            # Sum y values in the current x column
            sum = 0
            for y in range(pixels.shape[0]):
                sum += pixels[y][x]
            # Assign sum to the point (x, z) on the coronal image - p[z][x] in the pixel array, 
            # since z represents height (rows) and x represents length (columns)
            p[z][x] = sum / pixels.shape[0]
    else:
        # Remove alpha channel
        if pixels.shape[2] == 4:
            pixels = pixels[:,:,:-1]	
        for x in range(pixels.shape[1]):
            sum = np.zeros(pixels.shape[2])
            for y in range(pixels.shape[0]):
                new = np.zeros(pixels.shape[2])
                for i in range(pixels.shape[2]):
                    new[i] = pixels[y][x][i] + sum[i]
                sum = new
            p[z][x] = sum
    if z % 5 == 0:
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

sys.stdout.write("]\n")
            
# Save and display image
array = np.array(p, dtype=np.uint8)
xray = Image.fromarray(array)
xray.save('xray.png')
print('Xray saved to \'xray.png\'')
xray.show()
