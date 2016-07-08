#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os
import os.path as osp
import pprint
import shutil
import textwrap
import time
import shutil

import numpy as np
from scipy.ndimage import imread
from skimage.transform import resize
import matplotlib.pyplot as plt
from termcolor import cprint

from jsk_apc2016_common import get_object_data


target_names = ['no_object'] + [d['name'] for d in get_object_data()]

this_dir = osp.dirname(osp.abspath(__file__))
dataset_dir = osp.realpath(osp.join(this_dir, 'APC2016jsk/all'))

attempts = collections.defaultdict(list)
for target_label_name in target_names:
    if target_label_name != 'no_object':
        continue
    cprint("Scraping for '{}'".format(target_label_name), 'green')
    stamp_before = None
    stamp_start_view = None
    for dir_ in sorted(os.listdir(dataset_dir), key=lambda x: time.gmtime(int(x) * 1e-9)):
        stamp = time.gmtime(int(dir_) * 1e-9)

        if stamp_before is None:
            stamp_before = stamp
        if stamp_start_view is None:
            stamp_start_view = dir_

        label_name = open(osp.join(dataset_dir, dir_, 'label.txt')).read().strip()
        if label_name != target_label_name:
            continue
        if label_name not in target_names:
            print(osp.join(dataset_dir, dir_), label_name, img.shape[:2])
            raise ValueError

        hand_pose_file = osp.join(dataset_dir, dir_, 'hand_pose.yaml')
        if not osp.exists(hand_pose_file):
            continue

        img = imread(osp.join(dataset_dir, dir_, 'image.png'), mode='RGB')
        mask = imread(osp.join(dataset_dir, dir_, 'mask.png'), mode='L')
        mask = resize(mask, img.shape[:2], preserve_range=True).astype(np.uint8)
        applied = img.copy()
        applied[mask == 0] = 0
        h, w = img.shape[:2]
        if h * w < 10000:
            continue

        if (stamp_before is not None and (time.mktime(stamp) - time.mktime(stamp_before)) > 20):
            stamp_start_view = dir_
            # cprint('Maybe different picking trial', 'red')
        attempts[stamp_start_view].append(dir_)
        # print(time.strftime('%Y-%m-%d-%H-%M-%S', stamp), dir_)

        stamp_before = stamp

save_dir = osp.realpath(osp.join(this_dir, 'attempts'))
if not osp.exists(save_dir):
    os.mkdir(save_dir)
for attempt, views in attempts.items():
    os.mkdir(osp.join(save_dir, attempt))
    for view in views:
        shutil.copytree(osp.join(dataset_dir, view), osp.join(save_dir, attempt, view))
