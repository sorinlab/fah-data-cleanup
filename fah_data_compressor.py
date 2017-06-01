#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script compresses the Folding@Home data at the CLONE level.
Each clone is compressed and placed within its parent RUN folder.
For example,

PROJ1797/                      PROJ1797/
├── RUN0                       ├── RUN0
│   ├── CLONE0                 │   ├── CLONE0.ext
│   ├── CLONE1                 │   ├── CLONE1.ext
│   ├── CLONE10                │   ├── CLONE10.ext
│   ├── CLONE178    becomes    │   ├── CLONE178.ext
└── RUN1                       └── RUN1
│   ├── CLONE12                │   ├── CLONE12.ext
│   ├── CLONE13                │   ├── CLONE13.ext
│   └── CLONE15                │   └── CLONE15.ext
└── ...                        └── ...

where .ext is the compressed file extension.
"""

import argparse
import os
import re
from subprocess import call


class FAHDataCompressor(object):

    """Class for compressing F@H data."""

    def __init__(self, projectPath, maxDirs):
        """Initialization of class instance variables.

        Attributes:
            project_path    The project parent directory.
            max_dirs        The max number of directories to process.
        """
        self.project_path = projectPath
        self.max_dirs = maxDirs

    def find_clone_directories(self):
        """Find CLONE* directories inside the project.

        This function returns a list of tuples,
        each of which contains the path to the clone
        directory and the path to its parent directory.
        """
        clone_dirs = []
        project_root = os.path.abspath(self.project_path)
        for dir_name, subdir_list, _ in os.walk(project_root):
            if subdir_list and re.search(r'CLONE\d+$', dir_name) is None:
                # a CLONE dir has 'CLONE{x}' at the end of its path
                # and no subdir in it; if that's not the case,
                # continue without doing anything
                continue

            parent_dir = os.path.dirname(dir_name)
            name = dir_name[len(parent_dir + "/"):]
            clone_dirs.append((name, parent_dir))

        return clone_dirs

    def compress(self):
        """Start the compression job."""
        absolute_project_root = os.path.abspath(self.project_path)
        clone_dirs = self.find_clone_directories()

        processed_dir_count = 0
        for clone_dir_name, parent_dir in clone_dirs:
            processed_dir_count += 1
            if self.max_dirs is not None and processed_dir_count > self.max_dirs:
                break

            print 'Compressing %s/%s...' % (parent_dir, clone_dir_name),
            os.chdir(parent_dir)
            call(["tar", "cjfp", clone_dir_name + ".tar.bz2", clone_dir_name])
            call(["rm", "-rf", clone_dir_name])
            os.chdir(absolute_project_root)
            print 'Done!'

    def run(self):
        """Run the compression."""
        self.compress()


if __name__ == '__main__':
    ARGUMENT_PARSER = argparse.ArgumentParser()
    ARGUMENT_PARSER.add_argument('-p', '--project',
                                 metavar='PROJECT_PATH',
                                 required=True,
                                 dest='projectPath',
                                 help='path to the root of the F@H project')
    ARGUMENT_PARSER.add_argument('-m', '--max-dirs',
                                 type=int,
                                 metavar='NUM',
                                 dest='max_dirs_number',
                                 help='max number of directories to process')
    ARGS = ARGUMENT_PARSER.parse_args()
    COMPRESSOR = FAHDataCompressor(ARGS.projectPath, ARGS.max_dirs_number)
    COMPRESSOR.run()
