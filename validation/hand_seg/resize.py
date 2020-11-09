import glob
from PIL import Image
i = 0
for f in glob.glob("../images/*"):
    img = Image.open(f)
    img = img.resize((432,300))
    img.save('../images/vx' + str(i) + '.png')
    i += 1