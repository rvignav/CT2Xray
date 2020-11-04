from PIL import Image
import glob
import re
import numpy as np
import sys
import os
sys.setrecursionlimit(300000000)

global ret
ret = []
thresh = 1

def get_img(filename):
    final_img = Image.open(filename)
    return final_img

def floodfill(x, y):
    global matrix
    global ret
    if (matrix[x][y][0] > thresh and matrix[x][y][1] > thresh and matrix[x][y][2] > thresh): 
        matrix[x][y] = [0] 
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
            if (matrix[r][c][0] > thresh and matrix[r][c][1] > thresh and matrix[r][c][2] > thresh):
                ret.clear()
                floodfill(r, c)
                m = []
                for i in ret:
                    m.append(i)
                arr.append(m)
    return arr

def dice(imidx):
    mask_name = 'via_masks/mask' + str(imidx) + '.png'
    img = get_img(mask_name)
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

fnames = ['eval0.txt', 'eval1.txt']
vals = [0, 1]
for i in range(2):
    f = open(fnames[i], 'w')
    arr = dice(vals[i])
    f.write(str(arr))