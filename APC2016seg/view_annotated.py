#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path as osp

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import imread
from skimage.color import label2rgb

import jsk_apc2016_common


target_names = [None] * 256
target_names[0] = 'background'
for i, datum in enumerate(jsk_apc2016_common.get_object_data()):
    label_value = i + 1  # background is 0
    target_names[label_value] = datum['name']
target_names[255] = 'unlabeled'
target_names = np.array(target_names)

for dir_ in os.listdir('annotated'):
    img_file = osp.join('annotated', dir_, 'image.png')
    label_file = osp.join('annotated', dir_, 'label.png')
    img = imread(img_file, mode='RGB')
    label = imread(label_file, mode='L')
    print('{0}: candidates: {1}'.format(dir_, target_names[np.unique(label)]))
    label_viz = label2rgb(label, img, bg_label=0)
    label_viz[label == 255] = 0
    plt.imshow(label_viz)
    plt.show()
