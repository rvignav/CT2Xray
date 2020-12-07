import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import glob
import re
import time
import sys

def sort_list(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

scans = glob.glob('/Users/vignavramesh/Downloads/CT_Scans/*.nii')
scans = sort_list(scans)

for f in scans:
  if '_ct.nii' in f:
    mask = f.replace('_ct.nii', '_seg.nii')
    if mask not in scans:
        print(f)
        os.system('rm -rf ' + str(f))