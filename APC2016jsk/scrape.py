from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path as osp
import shutil

import numpy as np
from scipy.ndimage import imread
from skimage.transform import resize
import matplotlib.pyplot as plt


this_dir = osp.dirname(osp.abspath(__file__))
dataset_dir = osp.realpath(osp.join(this_dir, 'all'))
for dir_ in os.listdir(dataset_dir):
    img = imread(osp.join(dataset_dir, dir_, 'image.png'), mode='RGB')
    mask = imread(osp.join(dataset_dir, dir_, 'mask.png'), mode='L')
    mask = resize(mask, img.shape[:2], preserve_range=True).astype(np.uint8)
    label_name = open(osp.join(dataset_dir, dir_, 'label.txt')).read().strip()
    applied = img.copy()
    applied[mask == 0] = 0
    h, w = img.shape[:2]
    if h * w > 10000:
        continue
    print(osp.join(dataset_dir, dir_), label_name, img.shape[:2])
    plt.subplot(131)
    plt.imshow(img)
    plt.subplot(132)
    plt.imshow(mask, cmap='gray')
    plt.subplot(133)
    plt.imshow(applied)
    plt.show()

    while True:
        yn = raw_input('Remove?[yn]: ')
        if yn.lower() == 'y':
            shutil.rmtree(osp.join(dataset_dir, dir_))
        if yn.lower() in 'yn':
            break
