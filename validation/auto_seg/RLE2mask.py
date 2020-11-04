'''
https://www.kaggle.com/dmitrykonovalov/convert-run-length-encoding-to-png-mask-images?select=train_ship_segmentations_v2.csv
'''

import numpy as np 
import pandas as pd 
import os

df = pd.read_csv('input/pixels.csv')

img_names = df['ImageId'].unique()

import keras
from keras.preprocessing.image import save_img 

IMG_SHAPE = (1024, 1024)
OUTPUT_DIR = 'output'
# OUTPUT_DIR = '.'
# print('OUTPUT_DIR = ', OUTPUT_DIR)

# ref: https://www.kaggle.com/paulorzp/run-length-encode-and-decode
def rle_decode(mask_rle, shape=IMG_SHAPE):
    '''
    mask_rle: run-length as string formated (start length)
    shape: (height,width) of array to return
    Returns numpy array, 1 - mask, 0 - background
    '''
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape(shape).T  # Needed to align to RLE direction

for ImageId in img_names:
    # print('ImageId', ImageId)
    
    fname = ImageId.replace('.jpg', '.png')
    
    out_path = os.path.join(OUTPUT_DIR, fname)
    
    all_masks = np.zeros(IMG_SHAPE)
    # NOTE: multiple masks for the same image
    img_masks = df.loc[df['ImageId'] == ImageId, 'EncodedPixels'].tolist()
    for mask_rle in img_masks:
        if not pd.isnull(mask_rle):
            all_masks += rle_decode(mask_rle, shape=IMG_SHAPE)
        
    save_img(out_path, all_masks[..., np.newaxis])    # TODO: comment out to save to disk

    