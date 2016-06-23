from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import os
import os.path as osp
import re
import shlex
import subprocess
import sys
import tarfile
import zipfile


def extract_file(path, to_directory='.'):
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError("Could not extract '%s' as no appropriate "
                         "extractor is found" % path)
    cwd = os.getcwd()
    os.chdir(to_directory)
    try:
        file = opener(path, mode)
        try:
            file.extractall()
        finally:
            file.close()
    finally:
        os.chdir(cwd)


def download(client, url, output, quiet=False):
    cmd = '{client} {url} -O {output}'.format(client=client, url=url,
                                              output=output)
    if quiet:
        cmd += ' --quiet'
    subprocess.call(shlex.split(cmd))


def check_md5(path, md5):
    is_same = hashlib.md5(open(path, 'rb').read()).hexdigest() == md5
    return is_same


def is_google_drive_url(url):
    m = re.match('^https?://drive.google.com/uc\?id=.*$', url)
    return m is not None


def download_data(path, url, md5, download_client=None,
                  extract=False, quiet=True):
    """Install test data checking md5 and rosbag decompress if needed."""
    if download_client is None:
        if is_google_drive_url(url):
            download_client = 'gdown'
        else:
            download_client = 'wget'
    # check if cache exists, and update if necessary
    print("Checking md5 of '{path}'...".format(path=path))
    # check real path
    if osp.exists(path):
        if check_md5(path, md5):
            print("File '{0}' is newest.".format(path))
            if extract:
                print("Extracting '{path}'...".format(path=path))
                extract_file(path, to_directory=osp.dirname(path) or '.')
            return
        else:
            if not osp.islink(path):
                # not link and exists so skipping
                sys.stderr.write("WARNING: '{0}' exists\n".format(path))
                return
            os.remove(path)
    print("Downloading file from '{url}'...".format(url=url))
    download(download_client, url, path, quiet=quiet)
    if extract:
        print("Extracting '{path}'...".format(path=path))
        extract_file(path, to_directory=osp.dirname(path))
