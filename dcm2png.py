import glob
from PIL import Image
import pydicom as dicom
import os
import cv2

images = []
folders = glob.glob('/Users/vignavramesh/Downloads/COVID-19-AR/*')
for f in folders:
    studies = glob.glob(f + '/*')
    for s in studies:
        files = glob.glob(s + '/*')
        for fname in files:
            if (len(glob.glob(fname + '/*')) > 75):
                images.append(fname)

def bubble_sort(series):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(series) - 1):
            if series[i].SliceLocation > series[i + 1].SliceLocation:
                series[i], series[i + 1] = series[i + 1], series[i]
                swapped = True
    return series

for i in range(len(images)):
    series = images[i]
    dest_dir = '/Users/vignavramesh/Documents/scans/Volume' + str(i + 42) + '/'
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dcms = glob.glob(series + '/*.dcm')
    for idx in range(len(dcms)):
        dcms[idx] = dicom.read_file(dcms[idx])  
    dcms = bubble_sort(dcms)
    for count in range(len(dcms)):
        ds = dcms[count]
        p = ds.pixel_array
        cv2.imwrite(dest_dir + str(count) + ".jpg", p)