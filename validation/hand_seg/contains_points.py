from matplotlib.path import Path
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import mahotas
import json

all_x = []
all_y = []

with open('via_region_data.json') as f:
    data = json.load(f)

for img in data:
    all_x_i = []
    all_y_i = []
    d = data[img]
    regions = d['regions']
    for r in regions:
        all_x_i.append(r['shape_attributes']['all_points_x'])
        all_y_i.append(r['shape_attributes']['all_points_y'])
    all_x.append(all_x_i)
    all_y.append(all_y_i)

def render(xs, ys):
    X = int(300 * 1024/432)
    Y = int(432 * 1024/432)
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
        for i in range(len(xs)):
            xs[i] = int(xs[i] * 1024/432)
            ys[i] = int(ys[i] * 1024/432)
        mask = render(xs, ys)

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

    plt.imshow(p, cmap='gray')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig('via_masks/mask' + str(q) + '.png', bbox_inches = 'tight', pad_inches = 0)

    f = open('val' + str(q) + '.txt', 'w')
    f.write(str(arr))