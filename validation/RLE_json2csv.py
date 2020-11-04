import csv
import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys

with open('input/results.json') as f:
    data = json.load(f)
img_data = data["images"]

images = {}

for img in img_data:
    images[img["id"]] = img["file_name"]

annotations = data["annotations"]

with open('pixels.csv', mode='w') as pfile:
    writer = csv.writer(pfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['ImageId', 'EncodedPixels'])

    for img in annotations:
        fname = images[img["image_id"]]
        category = img["category_id"]

        try:
            counts = img["segmentation"]["counts"]
        except:
            continue

        if (len(counts) %2 == 1):
            counts = counts[:-1]

        string = ''
        for item in counts:
            string += str(item) + ' '
        string = string[:-1]
        
        writer.writerow([fname, string])