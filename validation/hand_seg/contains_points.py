from matplotlib.path import Path
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import mahotas

all_x_1 = [[147,119,91,47,35,77,106,123,131,144], [187,159,129,102,103,132,159,181], [356,315,318,296,296,296,304,329,375,388,388,388,392,360,377,370]]
all_y_1 = [[142,146,133,151,186,212,194,198,184,173], [75,58,68,88,102,111,109,106], [238,201,170,161,154,129,114,114,114,114,141,157,170,187,195,214]]

all_x_2 = [[185,148,137,120,119,149], [42,42,87,142,142,139,130,116,115,93,51,51], [292,308,295,280,277,277,293]]
all_y_2 = [[87,104,131,156,203,167], [196,237,249,249,230,213,208,195,158,147,147,165], [162,124,109,117,142,167,167]]

all_x = [all_x_1, all_x_2]
all_y = [all_y_1, all_y_2]

def render(xs, ys):
    X = 300
    Y = 432
    newPoly = [(ys[i], xs[i]) for i in range(len(xs))]  

    grid = np.zeros((X, Y), dtype=np.int8)
    mahotas.polygon.fill_polygon(newPoly, grid)
    # print(grid[147][142])
    return grid

for q in range(len(all_x)):
    p = None
    for idx in range(len(all_x[q])):
        xs = all_x[q][idx]
        ys = all_y[q][idx]
        mask = render(xs, ys)

        try:
            if (p == None):
                p = np.zeros(mask.shape)
        except:
            p = p
        
        for r in range(mask.shape[0]):
            for c in range(mask.shape[1]):
                if (mask[r][c]):
                    p[r][c] = 255

    plt.imshow(p, cmap='gray')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig('via_masks/mask' + str(q) + '.png', bbox_inches = 'tight', pad_inches = 0)