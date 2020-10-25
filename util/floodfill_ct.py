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

names = ['/Users/vignavramesh/Downloads/mask-slices/s-2-slice124..png', '/Users/vignavramesh/Downloads/mask-slices/s-2-slice140..png']

def dice(i):
    mask_name = names[i]
    img = Image.open(mask_name).convert('L')
    WIDTH, HEIGHT = img.size
    d = list(img.getdata()) 
    d = [d[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    global matrix
    matrix = np.asarray(d).astype(np.uint8)

    arr = flood()
    return arr

fnames = ['val0.txt', 'val1.txt']
for i in range(2):
    f = open(fnames[i], 'w')
    arr = dice(i)
    f.write(str(arr))
