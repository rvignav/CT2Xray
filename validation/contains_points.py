from matplotlib.path import Path
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import mahotas

all_x = [[147,119,91,47,35,77,106,123,131,144], [187,159,129,102,103,132,159,181], [356,315,318,296,296,296,304,329,375,388,388,388,392,360,377,370]]
all_y = [[142,146,133,151,186,212,194,198,184,173], [75,58,68,88,102,111,109,106], [238,201,170,161,154,129,114,114,114,114,141,157,170,187,195,214]]

def render(xs, ys):
    X = 300
    Y = 432
    newPoly = [(xs[i], ys[i]) for i in range(len(xs))]  

    grid = np.zeros((X, Y), dtype=np.int8)
    mahotas.polygon.fill_polygon(newPoly, grid)

    return grid

for p in range(len(all_x)):
    xs = all_x[p]
    ys = all_y[p]
    mask = render(xs, ys)
    im = Image.fromarray(mask)
    im.save("img.png")