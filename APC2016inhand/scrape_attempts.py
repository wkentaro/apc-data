#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path as osp

from scipy.ndimage import imread
import matplotlib.pyplot as plt


this_dir = osp.dirname(osp.realpath(__file__))
data_dir = osp.join(this_dir, 'attempts')
for attempt in os.listdir(data_dir):
    attempt_dir = osp.join(data_dir, attempt)
    imgs = []
    for view in os.listdir(attempt_dir):
        img = imread(osp.join(attempt_dir, view, 'image.png'), mode='RGB')
        imgs.append(img)
    n_imgs = len(imgs)
    for i, img in enumerate(imgs):
        plt.subplot(2, 3, i+1)
        plt.imshow(img)
        plt.axis('off')
    plt.show()
