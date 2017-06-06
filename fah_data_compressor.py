#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script compresses the Folding@Home data at the CLONE level.
Each clone is compressed and placed within its parent RUN folder.
For example,

PROJ1797/                      PROJ1797/
├── RUN0                       ├── RUN0
│   ├── CLONE0                 │   ├── CLONE0.ext
│   ├── CLONE1                 │   ├── CLONE1.ext
│   ├── CLONE10                │   ├── CLONE10.ext
│   ├── CLONE178    becomes    │   ├── CLONE178.ext
└── RUN1                       └── RUN1
│   ├── CLONE12                │   ├── CLONE12.ext
│   ├── CLONE13                │   ├── CLONE13.ext
│   └── CLONE15                │   └── CLONE15.ext
└── ...                        └── ...

where .ext is the compressed file extension.
"""

import argparse
import logging
import os
import re
import subprocess


class FAHDataCompressor(object):

    """Class for compressing F@H data."""

    def __init__(self, project_root, max_dirs, log_filename=None, log_level=None):
        """Initialization of class instance variables.

        Attributes:
            project_root    The project root, e.g. ../data/PROJ1797
            max_dirs        The max number of directories to process
            log_filename    Name of the log file, default to None
            log_level       Log level
        """
        logging.basicConfig(filename=log_filename, level=log_level or logging.INFO,
                            format='%(levelname)-5s %(asctime)s: %(message)s')

        self.project_root = project_root
        self.max_dirs = max_dirs

    @staticmethod
    def find_clone_directories(project_root):
        """Find CLONE* directories inside the project.

        This method returns a list of tuples,
        each of which contains the path to the clone
        directory and the path to its parent directory.
        """
        clone_dirs = []
        for dir_name, _, _ in os.walk(project_root):
            if re.search(r'CLONE\d+$', dir_name) is None:
                # a CLONE dir has 'CLONE*' at the end of its path,
                # e.g. /home/fahdata/PKNOT/simulation/PROJ1796
                # /RUN26/CLONE11; if that's not the case, continue
                # without doing anything
                continue

            parent_dir = os.path.dirname(dir_name)
            name = dir_name[len(parent_dir + "/"):]
            clone_dirs.append((name, parent_dir))

        return clone_dirs

    @staticmethod
    def compress_dir(clone_dir, parent_dir):
        """Compress a directory."""
        logger = logging.getLogger('logger')
        logger.info('Compressing %s/%s...', parent_dir, clone_dir)

        process = subprocess.Popen(
            'tar cjfpn %s.tar.bz2 %s' % (clone_dir, clone_dir),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        output, exit_code = process.communicate()
        if exit_code is not None and exit_code != 0:
            raise OSError('Cannot compress %s; tar exits with code %s\n%s'
                          % (clone_dir, exit_code, output.rstrip()))
        logger.info('Compressing %s/%s...Done', parent_dir, clone_dir)

    @staticmethod
    def remove_dir(clone_dir, parent_dir):
        """Remove a directory."""
        logger = logging.getLogger('logger')
        logger.info('Removing %s/%s...', parent_dir, clone_dir)
        subprocess.Popen('rm -rf %s' % clone_dir,
                         shell=True).communicate()
        logger.info('Removing %s/%s...Done', parent_dir, clone_dir)

    def compress(self):
        """Start the compression job."""
        logger = logging.getLogger('logger')

        absolute_project_root = os.path.abspath(self.project_root)
        clone_dirs = self.find_clone_directories(absolute_project_root)
        logger.info('Found %d clone directories in %s',
                    len(clone_dirs), self.project_root)

        if not clone_dirs:
            logger.info('There is no data to compress [exits]')
            return

        logger.info('Begin to compress %s', self.project_root)
        processed_dir_count = 0

        for clone_dir, parent_dir in clone_dirs:
            processed_dir_count += 1
            if self.max_dirs is not None and processed_dir_count > self.max_dirs:
                break
            try:
                os.chdir(parent_dir)
                self.compress_dir(clone_dir, parent_dir)
                self.remove_dir(clone_dir, parent_dir)
            except Exception as ex:
                logger.error('Unexpected error: %s', str(ex))
            finally:
                os.chdir(absolute_project_root)

        logger.info('Begin to compress %s...Done!', self.project_root)


if __name__ == '__main__':
    ARGUMENT_PARSER = argparse.ArgumentParser()
    ARGUMENT_PARSER.add_argument('project_root',
                                 metavar='PROJECT_ROOT',
                                 help='path to the root of the F@H project')
    ARGUMENT_PARSER.add_argument('-m', '--max-dirs',
                                 type=int,
                                 metavar='NUM',
                                 dest='max_dirs',
                                 help='max number of directories to process, '
                                 + 'useful for testing purposes')
    ARGUMENT_PARSER.add_argument('-l', '--log',
                                 metavar='LOG_FILENAME',
                                 dest='log_filename',
                                 help='name of file to log to')
    ARGUMENT_PARSER.add_argument('-v', '--verbosity',
                                 metavar='VERBOSITY',
                                 dest='log_level',
                                 help='indicates the level of verbosity to log.'
                                 + 'Possible values are:'
                                 + '\tINFO (includes all info, warning, and error logs);\n'
                                 + '\tWARN (include all warning and error logs);\n'
                                 + '\tERROR (include all error logs).\n'
                                 + 'If a log file is specified and a log level/verbosity'
                                 + 'is not set, it is default to INFO')

    ARGS = ARGUMENT_PARSER.parse_args()

    FAHDataCompressor(ARGS.project_root,
                      ARGS.max_dirs,
                      ARGS.log_filename,
                      ARGS.log_level).compress()
