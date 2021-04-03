from PIL import Image
import glob
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt 

d = glob.glob('/Users/vignavramesh/Documents/CT2Xray/tests/ground_truth_masks/*')
for i in d:
   im = Image.open(i)
   im = im.resize((1024,1024)) 
   im.save(i)
