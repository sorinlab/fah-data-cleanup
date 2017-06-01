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
# This is a test

class FAHDataCompressor(object):
    """Class for compressing F@H data."""
    def get_cli_arguments(self):
        """Get the command line arguments."""
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument('-p', '--project',
                                     metavar='PROJECT_PATH',
                                     required=True,
                                     dest='projectPath',
                                     help='path to the root of the F@H project')
        argument_parser.add_argument('-m', '--max-dirs',
                                     type=int,
                                     metavar='NUM',
                                     dest='max_dirs_number',
                                     help='max number of directories to process')
        return argument_parser.parse_args()

    def find_clone_directories(self, project_root):
        """Find CLONE* directories inside the project.

        This function returns a list of tuples,
        each of which contains the path to the clone
        directory and the path to its parent directory.
        """
        clone_dirs = []
        for dir_name, subdir_list, file_list in os.walk(project_root):
            if subdir_list and re.search(r'CLONE\d+$', dir_name) is None:
                # a CLONE dir has 'CLONE{x}' at the end of its path
                # and no subdir in it; if that's not the case,
                # continue without doing anything
                continue

            parent_dir = os.path.dirname(dir_name)
            name = dir_name[len(parent_dir + "/"):]
            clone_dirs.append((name, parent_dir))

        return clone_dirs

    def compress(self, project_root, max_dirs_number):
        """Start the compression job."""
        absolute_project_root = os.path.abspath(project_root)
        clone_dirs = self.find_clone_directories(absolute_project_root)

        processed_dir_count = 0
        for clone_dir_name, parent_dir in clone_dirs:
            processed_dir_count += 1
            if max_dirs_number is not None and processed_dir_count > max_dirs_number:
                break

            print 'Compressing %s/%s...' % (parent_dir, clone_dir_name),
            os.chdir(parent_dir)
            call(["tar", "cjfp", clone_dir_name + ".tar.bz2", clone_dir_name])
            call(["rm", "-rf", clone_dir_name])
            os.chdir(absolute_project_root)
            print 'Done!'

    def run(self):
        """Run the compression."""
        args = self.get_cli_arguments()
        project_root = args.projectPath
        max_dirs_number = args.max_dirs_number
        self.compress(project_root, max_dirs_number)


if __name__ == '__main__':
    FAHDataCompressor().run()
