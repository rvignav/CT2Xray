from PIL import Image
import glob
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt 

d = glob.glob('gt/*')
d2 = glob.glob('pr_xro/*')
d3 = glob.glob('pr_m/*')

d = sorted(d)
d2 = sorted(d2)
d3 = sorted(d3)

ious = []
ious2 = []

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

for i in range(len(d3)):
    im3 = Image.open(d3[i]).convert('L').resize((320,320))
    im1n = 'gt/' + str(d3[i][d3[i].rindex("pr_m/")+len("pr_m/"):])
    im2n = 'pr_xro/' + str(d3[i][d3[i].rindex("pr_m/")+ len("pr_m/"):])
    try:
        im1 = Image.open(im1n).convert('L').resize((320,320))
        im2 = Image.open(im2n).convert('L').resize((320,320))
    except:
        print(d3[i][d3[i].rindex("pr_m/")+ len("pr_m/"):])

    HEIGHT, WIDTH = im1.size
    data = list(im1.getdata())
    pixels = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

    data2 = list(im2.getdata())
    pixels2 = [data2[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    
    data3 = list(im3.getdata())
    pixels3 = [data3[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

    u = 0
    n1 = 0
    n2 = 0

    for r in range(len(pixels)):
        for c in range(len(pixels[r])):
            u += 1
            if (pixels[r][c] == pixels2[r][c]):
                n1 += 1
            if (pixels[r][c] == pixels3[r][c]):
                n2 += 1

    ious.append((n1)/(u+u-n1))
    ious2.append((n2)/(u+u-n2))

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return str(round(m,4)) + " +/- " + str(round(h,4)) + " = " + str((round(m-h,4),round(m+h,4)))

print("X-rays Only: " + mean_confidence_interval(ious))
print("Mixed: " + mean_confidence_interval(ious2))