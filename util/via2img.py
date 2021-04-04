from matplotlib.path import Path
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import mahotas
import os
import json

if not os.path.exists('masks'):
    os.mkdir('masks')

all_x = []
all_y = []
names = []

with open('/Users/vignavramesh/Downloads/via_region_data.json') as f:
    data = json.load(f)

for img in data:
    all_x_i = []
    all_y_i = []
    d = data[img]
    regions = d['regions']
    names.append(d['filename'])
    for r in regions:
        all_x_i.append(r['shape_attributes']['all_points_x'])
        all_y_i.append(r['shape_attributes']['all_points_y'])
    all_x.append(all_x_i)
    all_y.append(all_y_i)

def render(q, xs, ys):
    img = Image.open('/Users/vignavramesh/Documents/CT2Xray/mixed/train/' + names[q])
    X = img.size[1]
    Y = img.size[0]
    newPoly = [(ys[i], xs[i]) for i in range(len(xs))]  
    grid = np.zeros((X, Y), dtype=np.int8)
    mahotas.polygon.fill_polygon(newPoly, grid)
    return grid

for q in range(len(all_x)):
    arr = []
    p = None
    for idx in range(len(all_x[q])):
        xs = all_x[q][idx]
        ys = all_y[q][idx]
        mask = render(q, xs, ys)

        try:
            if (p == None):
                p = np.zeros(mask.shape)
        except:
            p = p
        
        m = []

        for r in range(mask.shape[0]):
            for c in range(mask.shape[1]):
                if (mask[r][c]):
                    p[r][c] = 255
                    m.append((r,c))
        
        arr.append(m)

    im = Image.fromarray(p)
    im.convert("L").save('masks/' + names[q])