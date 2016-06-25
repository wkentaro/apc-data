#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import subprocess

import argparse
import base64
import cStringIO as StringIO
import json
import os
import os.path as osp
import shutil
import tempfile

import numpy as np
import PIL
import PIL.Image
import PIL.ImageDraw
from scipy.misc import imsave
from scipy.ndimage import imread
from skimage.color import label2rgb

import jsk_apc2016_common


def labelcolormap(N=256):

    def bitget(byteval, idx):
        return ((byteval & (1 << idx)) != 0)

    cmap = np.zeros((N, 3))
    for i in xrange(0, N):
        id = i
        r, g, b = 0, 0, 0
        for j in xrange(0, 8):
            r = np.bitwise_or(r, (bitget(id, 0) << 7-j))
            g = np.bitwise_or(g, (bitget(id, 1) << 7-j))
            b = np.bitwise_or(b, (bitget(id, 2) << 7-j))
            id = (id >> 3)
        cmap[i, 0] = r
        cmap[i, 1] = g
        cmap[i, 2] = b
    cmap = cmap.astype(np.float32) / 255
    return cmap


def json_to_label(json_file):
    data = json.load(open(json_file))
    # string -> numpy.ndarray
    f = StringIO.StringIO()
    f.write(base64.b64decode(data['imageData']))
    img = np.array(PIL.Image.open(f))
    # polygon array -> label
    label = np.zeros(img.shape[:2], dtype=np.int32)
    for shape in data['shapes']:
        # polygon -> mask
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = map(tuple, shape['points'])
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask)
        # fill label value
        label[mask == 1] = shape['label']
    return label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rawdata_dir')
    parser.add_argument('dataset_dir')
    args = parser.parse_args()

    rawdata_dir = args.rawdata_dir
    dataset_dir = args.dataset_dir

    target_names = ['background'] + \
        [obj['name'] for obj in jsk_apc2016_common.get_object_data()]
    for label_id, label_name in enumerate(target_names):
        print('{0}: {1}'.format(label_id, label_name))

    tmp_dir = tempfile.mkdtemp()
    if not osp.exists(tmp_dir):
        os.makedirs(tmp_dir)

    raw_archive_dir = rawdata_dir + '_archive'
    if not osp.exists(raw_archive_dir):
        os.makedirs(raw_archive_dir)

    cmap = labelcolormap(len(target_names))

    for dir_ in os.listdir(rawdata_dir):
        img_file = osp.join(rawdata_dir, dir_, 'image.png')
        bin_mask_file = osp.join(rawdata_dir, dir_, 'bin_mask.png')
        json_file = osp.join(tmp_dir, 'labelme.json')
        cmd = 'labelme {0} -O {1}'.format(img_file, json_file)
        subprocess.call(cmd, shell=True)

        save_dir = osp.join(dataset_dir, dir_)
        if not osp.exists(save_dir):
            os.makedirs(save_dir)
        shutil.copy(img_file, osp.join(save_dir, 'image.png'))

        label = json_to_label(json_file)
        bin_mask = imread(bin_mask_file, mode='L')
        label[bin_mask == 0] = 255
        imsave(osp.join(save_dir, 'label.png'), label)

        label_viz = label2rgb(label, colors=cmap)
        imsave(osp.join(save_dir, 'label_viz.png'), label_viz)

        shutil.move(osp.join(rawdata_dir, dir_), raw_archive_dir)


if __name__ == '__main__':
    main()
