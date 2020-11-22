from PIL import Image
import glob

d = glob.glob('masks/*')
arr = []
for i in d:
    img = Image.open(i).convert('L')  # convert image to 8-bit grayscale
    HEIGHT, WIDTH = img.size
    data = list(img.getdata()) # convert image data to a list of integers
    # convert that to 2D list (list of lists of integers)
    pixels = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    r = len(pixels)
    c = len(pixels[0])
    arr.append((r,c))

print(len(arr))
print(arr)
    