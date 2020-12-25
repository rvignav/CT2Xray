from PIL import Image
import glob

d = glob.glob('/Users/vignavramesh/Documents/CT2Xray/tests/ground_truth_masks/*')
d2 = glob.glob('/Users/vignavramesh/Documents/CT2Xray/tests/xrays_only_masks/*')
d3 = glob.glob('/Users/vignavramesh/Documents/CT2Xray/tests/mixed_masks/*')

d = sorted(d)
d2 = sorted(d2)
d3 = sorted(d3)

dices = []
dices2 = []

for i in range(len(d)):
    im1 = Image.open(d[i]).convert('L')
    im2 = Image.open(d2[i]).convert('L')
    im3 = Image.open(d3[i]).convert('L')
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

    dices.append((2*n1)/(u+u))
    dices2.append((2*n2)/(u+u))

print("DICE (X-rays Only): " + str(sum(dices)/len(dices)))
print("DICE (Mixed): " + str(sum(dices2)/len(dices2)))
    