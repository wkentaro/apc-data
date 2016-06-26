from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os
import os.path as osp
import pprint
import shutil
import textwrap

import numpy as np
from scipy.ndimage import imread
from skimage.transform import resize
import matplotlib.pyplot as plt

from jsk_apc2016_common import get_object_data


target_names = ['no_object'] + [d['name'] for d in get_object_data()]

this_dir = osp.dirname(osp.abspath(__file__))
dataset_dir = osp.realpath(osp.join(this_dir, 'all'))
stats = collections.defaultdict(int)
for dir_ in os.listdir(dataset_dir):
    img = imread(osp.join(dataset_dir, dir_, 'image.png'), mode='RGB')
    mask = imread(osp.join(dataset_dir, dir_, 'mask.png'), mode='L')
    mask = resize(mask, img.shape[:2], preserve_range=True).astype(np.uint8)
    label_name = open(osp.join(dataset_dir, dir_, 'label.txt')).read().strip()
    if label_name not in target_names:
        print(osp.join(dataset_dir, dir_), label_name, img.shape[:2])
        raise ValueError
    applied = img.copy()
    applied[mask == 0] = 0
    h, w = img.shape[:2]
    # if h * w > 10000:
    #     continue
    stats[label_name] += 1

    # plt.subplot(131)
    # plt.imshow(img)
    # plt.subplot(132)
    # plt.imshow(mask, cmap='gray')
    # plt.subplot(133)
    # plt.imshow(applied)
    # plt.show()

    # while True:
    #     yn = raw_input('Remove?[yn]: ')
    #     if yn.lower() == 'y':
    #         shutil.rmtree(osp.join(dataset_dir, dir_))
    #     if yn.lower() in 'yn':
    #         break
for label_name in target_names:
    number = stats[label_name]
    print('{0}: {1}'.format(' ' * (40 - len(label_name)) + label_name, number))
