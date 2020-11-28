from PIL import Image
import glob
import re
import numpy as np
import sys
import os
sys.setrecursionlimit(300000000)

import subprocess

def install(package):
    subprocess.check_call([sys.executable, '-m', "pip", "install", package])

def install_arg(package, arg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", arg, package])

global ret
ret = []
thresh = 50

def sort_list(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

def create_image(dirname, label):
    if dirname[-1] == "/":
        dirname = dirname[:-1]
    images = glob.glob(str(dirname) + "/*.png")

    # Sort images alphanumerically by filename to ensure that z loops from front to back
    images = sort_list(images)

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

    filename = 'img.jpg'

    array = np.array(p, dtype=np.uint8)
    xray = Image.fromarray(array)
    xray.save(filename)
    
    final_img = Image.open(filename)
    size = 300
    if final_img.size[1] < 300:
        final_img = final_img.resize((final_img.size[0], 300))    

    final_img.save(filename)

    ret = []
    ret.append(final_img)
    ret.append(len(images))

    return ret

def floodfill(x, y):
    global matrix
    global ret
    if matrix[x][y] > thresh: 
        matrix[x][y] = 0 
        ret.append((x,y))
        if x > 0:
            floodfill(x-1,y)
        if x < matrix.shape[0] - 1:
            floodfill(x+1,y)
        if y > 0:
            floodfill(x,y-1)
        if y < matrix.shape[1] - 1:
            floodfill(x,y+1)

def flood():
    global matrix
    global ret
    ret.clear()
    arr = []
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            if (matrix[r][c] > thresh):
                ret.clear()
                floodfill(r, c)
                m = []
                for i in ret:
                    m.append(i)
                arr.append(m)
    return arr

def dice(imidx):
    mask_name = 'data/masks/Volume' + str(imidx)
    ret = create_image(mask_name, 'Calculating DICE coefficient for image ' + str(imidx) + ':')
    img = ret[0]
    W, H = img.size
    new_size = int(H * 1024 / W)
    img = img.resize((1024, new_size))

    WIDTH, HEIGHT = img.size
    d = list(img.getdata()) 
    d = [d[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    global matrix
    matrix = np.asarray(d).astype(np.uint8)

    arr = flood()
    return arr

for i in range(42):
    f = open('val' + str(i) + '.txt', 'w')
    arr = dice(i)
    f.write(str(arr))
