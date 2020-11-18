import os
import json
import random
import numpy as np
import re
import sys
import requests
from io import BytesIO
import base64
import glob
from math import trunc
from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
import matplotlib.pyplot as plt
from ConcaveHull import ConcaveHull

ret = []

thresh = 200

def floodfill(x, y):
    if matrix[x][y] > thresh: 
        matrix[x][y] = 0 
        ret.append((x,y))
        if x > 0:
            floodfill(x-1,y)
        if x < matrix.shape[0] - 1:
            floodfill(x+1,y)
        if y > 0:
            floodfill(x,y-1)
        if y < matrix.shape[1] - 1:
            floodfill(x,y+1)

def flood():
    arr = []
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            if (matrix[r][c] > thresh):
                ret.clear()
                floodfill(r, c)
                m = []
                for i in ret:
                    m.append(i)
                arr.append(m)
    return arr

sys.setrecursionlimit(300000)
data = {}

def show(arr, index):
    ans = [] 
    a = arr[index]
    x = []
    y = []
    for tup in a:
      x.append(tup[0])
      y.append(tup[1])
    allPoints=np.column_stack((x,y))
    ch = ConcaveHull()
    ch.loadpoints(allPoints)
    ch.calculatehull()
    boundary_points = np.vstack(ch.boundary.exterior.coords.xy).T
    xs = []
    ys = []
    for r in range(len(boundary_points)):
        ans.append((boundary_points[r][0], boundary_points[r][1]))
        xs.append(boundary_points[r][0])
        ys.append(boundary_points[r][1])
    return ans

class CocoDataset():
    def __init__(self, annotation_path, image_dir):
        self.annotation_path = annotation_path
        self.image_dir = image_dir
        self.colors = colors = ['blue', 'purple', 'red', 'green', 'orange', 'salmon', 'pink', 'gold',
                                'orchid', 'slateblue', 'limegreen', 'seagreen', 'darkgreen', 'olive',
                               'teal', 'aquamarine', 'steelblue', 'powderblue', 'dodgerblue', 'navy',
                               'magenta', 'sienna', 'maroon']
        
        json_file = open(self.annotation_path)
        self.coco = json.load(json_file)
        json_file.close()
        
        self.process_info()
        self.process_licenses()
        self.process_categories()
        self.process_images()
        self.process_segmentations()
    
    def display_image(self, image_id, fname, show_polys=True, show_bbox=True, show_crowds=True, use_url=False):
        if os.path.exists('masks/' + str(fname[:fname.rindex('.')]) + '.png'):
            return

        # print('Image:')
        # print('======')
        # if image_id == 'random':
        #     image_id = random.choice(list(self.images.keys()))
        
        # # Print the image info
        image = self.images[image_id]
        # for key, val in image.items():
        #     print('  {}: {}'.format(key, val))
            
        # Open the image
        if use_url:
            image_path = image['coco_url']
            response = requests.get(image_path)
            image = PILImage.open(BytesIO(response.content))
            
        else:
            image_path = os.path.join(self.image_dir, image['file_name'])
            image = PILImage.open(image_path)
            
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            
            data_uri = base64.b64encode(buffer.read()).decode('ascii')
            image_path = "data:image/png;base64,{0}".format(data_uri)
            
        # Calculate the size and adjusted display size
        image_width, image_height = image.size
        max_width = image_width
        adjusted_width = min(image_width, max_width)
        adjusted_ratio = adjusted_width / image_width
        adjusted_height = adjusted_ratio * image_height
        
        # Create list of polygons to be drawn
        polygons = {}
        bbox_polygons = {}
        rle_regions = {}
        poly_colors = {}
        # print('  segmentations ({}):'.format(len(self.segmentations[image_id])))
        for i, segm in enumerate(self.segmentations[image_id]):
            polygons_list = []
            if segm['category_id'] != 3 and segm['category_id'] != 6:
               continue
            if segm['iscrowd'] != -5000:
                px = 0
                x, y = 0, 0
                rle_list = []
                for j, counts in enumerate(segm['segmentation']['counts']):
                    if j % 2 == 0:
                        # Empty pixels
                        px += counts
                    else:
                        # Need to draw on these pixels, since we are drawing in vector form,
                        # we need to draw horizontal lines on the image
                        x_start = trunc(trunc(px / image_height) * adjusted_ratio)
                        y_start = trunc(px % image_height * adjusted_ratio)
                        px += counts
                        x_end = trunc(trunc(px / image_height) * adjusted_ratio)
                        y_end = trunc(px % image_height * adjusted_ratio)
                        if x_end == x_start:
                            # This is only on one line
                            rle_list.append({'x': x_start, 'y': y_start, 'width': 1 , 'height': (y_end - y_start)})
                        if x_end > x_start:
                            # This spans more than one line
                            # Insert top line first
                            rle_list.append({'x': x_start, 'y': y_start, 'width': 1, 'height': (image_height - y_start)})
                            
                            # Insert middle lines if needed
                            lines_spanned = x_end - x_start + 1 # total number of lines spanned
                            full_lines_to_insert = lines_spanned - 2
                            if full_lines_to_insert > 0:
                                full_lines_to_insert = trunc(full_lines_to_insert * adjusted_ratio)
                                rle_list.append({'x': (x_start + 1), 'y': 0, 'width': full_lines_to_insert, 'height': image_height})
                                
                            # Insert bottom line
                            rle_list.append({'x': x_end, 'y': 0, 'width': 1, 'height': y_end})
                if len(rle_list) > 0:
                    rle_regions[segm['id']] = rle_list  
            else:
                for segmentation_points in segm['segmentation']: #['counts']
                    segmentation_points = np.multiply(segmentation_points, adjusted_ratio).astype(int)
                    polygons_list.append(str(segmentation_points).lstrip('[').rstrip(']'))
            polygons[segm['id']] = polygons_list
            if i < len(self.colors):
                poly_colors[segm['id']] = self.colors[i]
            else:
                poly_colors[segm['id']] = 'white'
            
            bbox = segm['bbox']
            bbox_points = [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1],
                           bbox[0] + bbox[2], bbox[1] + bbox[3], bbox[0], bbox[1] + bbox[3],
                           bbox[0], bbox[1]]
            bbox_points = np.multiply(bbox_points, adjusted_ratio).astype(int)
            bbox_polygons[segm['id']] = str(bbox_points).lstrip('[').rstrip(']')
                
        if show_crowds:
            mask_arr = np.zeros((image_height, image_width))
            arr = []
            for seg_id, rect_list in rle_regions.items():
                m = []
                for rect_def in rect_list:
                    x, y = rect_def['x'], rect_def['y']
                    w, h = rect_def['width'], rect_def['height']
                    for r in range(x, x+w+1):
                        for c in range(y,y+h+1):
                            m.append((c,r))
                arr.append(m)
            
            l = float(300)
            # global matrix
            # matrix = mask_arr.astype(np.uint8)
            # l = float(l)
            # arr = flood()
        
            size = int(l * 21.5895 + 5965.85)
            name = fname + str(size)
            
            regions = []
            
            for idx in range(len(arr)):
                t = arr[idx]
                if (min(t)[0] == max(t)[0] or min(t, key = lambda q: q[1])[1] == max(t, key = lambda q: q[1])[1]):
                    continue
                a = show(arr, idx)
                all_points_x = []
                all_points_y = []
                for tup in a:
                    all_points_x.append(int(tup[0]))
                    all_points_y.append(int(tup[1]))
            
                shape_attributes = {}
                shape_attributes['name'] = 'polygon'
                shape_attributes['all_points_x'] = all_points_y
                shape_attributes['all_points_y'] = all_points_x

                image_quality = {}
                image_quality['good'] = True
                image_quality['frontal'] = True
                image_quality['good_illumination'] = True

                region_attributes = {}
                region_attributes['name'] = 'not_defined'
                region_attributes['type'] = 'unknown'
                region_attributes['image_quality'] = image_quality
                
                regions.append({
                    'shape_attributes':shape_attributes,
                    "region_attributes": region_attributes
                })

            file_attributes = {}
            file_attributes['caption'] = ''
            file_attributes['public_domain'] = 'no'
            file_attributes['image_url'] = ''

            data[name] = {}
            data[name]['filename'] = fname
            data[name]['size'] = size
            data[name]['regions'] = regions
            data[name]['file_attributes'] = file_attributes

            #                 mask_arr[c][r] = 255
            # plt.imshow(mask_arr, cmap='gray')
            # plt.gca().set_axis_off()
            # figure = plt.gcf()
            # figure.set_size_inches(mask_arr.shape[0], mask_arr.shape[1])
            # plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
            # plt.margins(0,0)
            # plt.gca().xaxis.set_major_locator(plt.NullLocator())
            # plt.gca().yaxis.set_major_locator(plt.NullLocator())
            # plt.savefig('masks/' + str(fname[:fname.rindex('.')]) + '.png', bbox_inches = 'tight', pad_inches = 0, dpi=1)
            # im1 = PILImage.open('masks/' + str(fname[:fname.rindex('.')]) + '.png')
            # im1 = im1.resize((image_width, image_height))
            # im1.save('masks/' + str(fname[:fname.rindex('.')]) + '.png')
            # plt.close()

    def process_info(self):
        self.info = self.coco['info']
    
    def process_licenses(self):
        self.licenses = self.coco['licenses']
    
    def process_categories(self):
        self.categories = {}
        self.super_categories = {}
        for category in self.coco['categories']:
            cat_id = category['id']
            super_category = category['supercategory']
            
            # Add category to the categories dict
            if cat_id not in self.categories:
                self.categories[cat_id] = category
            else:
                print("ERROR: Skipping duplicate category id: {}".format(category))

            # Add category to super_categories dict
            if super_category not in self.super_categories:
                self.super_categories[super_category] = {cat_id} # Create a new set with the category id
            else:
                self.super_categories[super_category] |= {cat_id} # Add category id to the set
                
    def process_images(self):
        self.images = {}
        for image in self.coco['images']:
            image_id = image['id']
            if image_id in self.images:
                print("ERROR: Skipping duplicate image id: {}".format(image))
            else:
                self.images[image_id] = image
                
    def process_segmentations(self):
        self.segmentations = {}
        for segmentation in self.coco['annotations']:
            image_id = segmentation['image_id']
            if image_id not in self.segmentations:
                self.segmentations[image_id] = []
            self.segmentations[image_id].append(segmentation)

annotation_path = './sample_annotations.json'
image_dir = '../images'

coco_dataset = CocoDataset(annotation_path, image_dir)

if not os.path.exists('masks'):
    os.makedirs('masks')

count = 50

d = glob.glob('../images/*')
for i in d:
    if count < 0:
        break
    count -= 1
    fname = i[i.rindex('images/') + len('images/'):]
    idx = -1
    for img in coco_dataset.images:
        if fname == coco_dataset.images[img]['file_name']:
            idx = img
            break
    if idx == -1:
        continue
    coco_dataset.display_image(idx, fname, show_polys=False, show_bbox=False, show_crowds=True, use_url=False)

with open('via_region_data.json', 'w') as outfile:
    json.dump(data, outfile)