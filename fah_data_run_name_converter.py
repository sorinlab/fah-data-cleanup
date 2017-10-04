#!/usr/bin/env python

""" Renumber all RUN folders of a F@H dataset to correspond to RMSD.
    For instance, RUN0 will be the lowest in RMSD (Angstrom)
    and RUN N should be the highest in RMSD.
    The script accepts the working directory of the data Proj<#>
    and a .csv with the mapping values in the following format:

        OLD RUN, RMSD, NEW RUN
"""
import argparse
import os
import re


def valid_file(path):
    """ Function to check the existence of a file.
        Used in conjunction with argparse to check that the given parameter
        files exist.
    """
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            '\"{}\" does not exist'.format(path) +
            '(must be in the same directory or specify full path).')
    return path


def valid_dir(path):
    """ Function to check the existence of a directory.
        Used in conjunction with argparse to check that the given parameter
        dataset exist.
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(
            '\"{}\" does not exist'.format(path) +
            '(must be in the same directory or specify full path).')
    return path


class FAHDataRunNameConverter(object):

    """Class for renumbering all RUN folders of a F@H dataset to correspond to RMSD."""

    def __init__(self, working_directory, mapper, dry_run=False):
        if not os.path.isdir(working_directory):
            raise OSError(
                2, 'No such file or directory', working_directory)
        self.working_directory = working_directory
        if not os.path.isfile(mapper):
            raise OSError(2, 'No such file or directory', mapper)
        self.mapper = mapper
        self.mapper_dict = self.create_mapper_dict()
        self.dry_run = dry_run

    def create_mapper_dict(self):
        """Method to create the mapper dictionary"""
        mapper_file = open(self.mapper, mode='r')
        mapper_lines = mapper_file.readlines()
        mapper_line_splits = [line.rstrip().split(',')
                              for line in mapper_lines if not line.lstrip().startswith('#')]
        mapper_dict = {line_split[0]: (line_split[1], line_split[2])
                       for line_split in mapper_line_splits}
        return mapper_dict

    def display_mapper_info(self):
        """Method that displays mapper input information."""
        print '{0}Mapper Information{0}'.format('-' * 6)
        format_string = '{:<10}{:<10}{:<10}'
        print format_string.format('OLD RUN', 'RMSD', 'NEW RUN')
        for key, value in self.mapper_dict.iteritems():
            print format_string.format(key, value[0], value[1])

    def run_dir_generator(self):
        """Method to genenerate run directories."""
        working_directory_walk = os.walk(self.working_directory)
        for root, _, _ in working_directory_walk:
            if 'RUN' in root:
                if 'CLONE' not in root:
                    yield root
            else:
                continue

    def convert_generator(self):
        """Method to genenerate conversion values."""
        for directory in self.run_dir_generator():
            directory_search = re.search(r'(?<=RUN)\d+', directory)
            if directory_search is not None:
                directory_run_num = directory_search.group(0)
                new_run_number = self.mapper_dict.get(directory_run_num)[1]
                new_run_dir = directory.replace(
                    'RUN{}'.format(directory_run_num),
                    'RUN{}'.format(new_run_number))
                yield directory, new_run_dir
            else:
                continue

    def display_dry_run_info(self):
        """Method to display dry-run information."""
        print '{0}Dryrun Information{0}'.format('-' * 6)
        for directory, new_run_dir in self.convert_generator():
            print '{:<26} -> {}'.format(directory, new_run_dir)
            self.clone_cleanup_dry_run(directory, new_run_dir)

    def clone_cleanup_dry_run(self, directory, new_run_dir):
        """Method to display dry-run clone cleanup information."""
        clone_walk = os.walk(directory)
        for root, _, files in clone_walk:
            base_dir = root.split("/")[-1]
            if "RUN" in base_dir:
                continue
            else:
                new_run_clone_path = os.path.join(new_run_dir, base_dir)
                prc = self.extract_prc(new_run_clone_path)
            xtc_cleanup = []
            pdb_cleanup = []
            for f in files:
                if f.endswith(".xtc"):
                    xtc_cleanup.append(os.path.join(root, f))
                if f.endswith(".pdb"):
                    pdb_cleanup.append(os.path.join(root, f))
            xtc_cleanup_size = len(xtc_cleanup)
            if xtc_cleanup_size > 1:
                print '{0}ERROR{0}-'.format('-' * 12)
                print 'More than one .xtc file in {}'.format(root)
                print 'Cannot clean up .xtc.'
                print '{}'.format('-' * 30)
            elif xtc_cleanup_size < 1:
                print '{0}ERROR{0}-'.format('-' * 12)
                print 'No .xtc file in {}'.format(root)
                print 'No .xtc to cleanup.'
                print '{}'.format('-' * 30)
            elif xtc_cleanup_size == 1:
                xtc_original_path = xtc_cleanup[0]
                xtc_new_name = "P{0}_R{1}_C{2}.xtc".format(*prc)
                xtc_new_path = os.path.join(new_run_clone_path, xtc_new_name)
                print '\t{0:<26} -> {1}'.format(xtc_original_path, xtc_new_path)
                for pdb in pdb_cleanup:
                    pdb_frame_and_ext = pdb.split("/")[-1].split("_")[-1]
                    new_pdb_name = "p{0[0]}_r{0[1]}_c{0[2]}_{1}".format(prc, pdb_frame_and_ext)
                    new_pdb_path = os.path.join(new_run_clone_path, new_pdb_name)
                    print '\t\t{0:<26} -> {1}'.format(pdb, new_pdb_path)

    def stage_rename(self):
        """Method for staging the rename of RUN folders to RMSD-determined name."""
        for directory, new_run_dir in self.convert_generator():
            new_root_temp = '{}.tmp'.format(new_run_dir)
            try:
                os.rename(directory, new_root_temp)
            except OSError:
                print '{0}ERROR{0}-'.format('-' * 12)
                print '{:<26} -x> {}'.format(directory, new_root_temp)
                print '{} already exists.'.format(new_root_temp)
                print '{}'.format('-' * 30)

    def finalize_rename(self):
        """Method to finalize the rename of RUN folders to RMSD-determined name."""
        for directory in self.run_dir_generator():
            directory_replace = directory.replace('.tmp', '')
            try:
                os.rename(directory, directory_replace)
                self.clone_cleanup(directory_replace)
            except OSError:
                print '{0}ERROR{0}-'.format('-' * 12)
                print '{:<26} -x> {}'.format(directory, directory_replace)
                print '{} already exists.'.format(directory_replace)
                print '{}'.format('-' * 30)

    def clone_cleanup(self, directory):
        """Method to clean up .xtc files in clone directories"""
        clone_walk = os.walk(directory)
        for root, _, files in clone_walk:
            if "RUN" in root.split("/")[-1]:
                continue
            else:
                prc = self.extract_prc(root)
            xtc_cleanup = []
            for f in files:
                if f.endswith(".xtc"):
                    xtc_cleanup.append(f)
                if f.endswith(".pdb"):
                    pdb_frame_and_ext = f.split("_")[-1]
                    pdb_original_path = os.path.join(root, f)
                    pdb_new_name = "p{0[0]}_r{0[1]}_c{0[2]}_{1}".format(
                        prc, pdb_frame_and_ext)
                    pdb_new_name_path = os.path.join(root, pdb_new_name)
                    try:
                        os.rename(pdb_original_path, pdb_new_name_path)
                    except OSError as oerror:
                        print '{0}ERROR{0}-'.format('-' * 12)
                        print "{} -> {}".format(pdb_original_path, pdb_new_name_path)
                        print '{}'.format(oerror.strerror)
                        print '{}'.format('-' * 30)
            xtc_cleanup_size = len(xtc_cleanup)
            if xtc_cleanup_size > 1:
                print '{0}ERROR{0}-'.format('-' * 12)
                print 'More than one .xtc file in {}'.format(root)
                print 'Cannot clean up .xtc.'
                print '{}'.format('-' * 30)
            elif xtc_cleanup_size < 1:
                print '{0}ERROR{0}-'.format('-' * 12)
                print 'No .xtc file in {} to clean up'.format(root)
                print '{}'.format('-' * 30)
            elif xtc_cleanup_size == 1:
                xtc_original_path = os.path.join(root, xtc_cleanup[0])
                xtc_new_name = "P{0}_R{1}_C{2}.xtc".format(*prc)
                xtc_rename_path = os.path.join(root, xtc_new_name)
                try:
                    os.rename(xtc_original_path, xtc_rename_path)
                except OSError as oerror:
                    print '{0}ERROR{0}-'.format('-' * 12)
                    print "{} -> {}".format(xtc_original_path, xtc_rename_path)
                    print '{}'.format(oerror.strerror)
                    print '{}'.format('-' * 30)

    @staticmethod
    def extract_prc(directory):
        """Static method to extract project, run, clone values from path."""
        dir_split = directory.split("/")
        for split in dir_split:
            if "PROJ" in split:
                proj_val = split[4:]
            elif "RUN" in split:
                run_val = split[3:]
            elif "CLONE" in split:
                clone_val = split[5:]
        return (proj_val, run_val, clone_val)

    def convert(self):
        """Method to renumber all RUN folders of a F@H dataset to correspond to RMSD."""
        self.stage_rename()
        self.finalize_rename()

    def __main__(self):
        """The RUN folder converter."""
        if self.dry_run:
            self.display_mapper_info()
            print '-' * 30
            self.display_dry_run_info()
            print '-' * 30
        else:
            self.convert()
        print 'Done.'


if __name__ == '__main__':
    MODULE_DESCRIPTION = str("Renumber all RUN folders of a F@H dataset to correspond to RMSD.\n" +
                             "For instance, RUN0 will be the lowest in RMSD (Angstrom)\n" +
                             "and RUN N should be the highest in RMSD.\n" +
                             "The script accepts the working directory of the data Proj<#>\n" +
                             "and a .csv with the mapping values in the following format:\n\n" +
                             "OLD RUN, RMSD, NEW RUN")
    ARGUMENT_PARSER = argparse.ArgumentParser(description=MODULE_DESCRIPTION,
                                              formatter_class=argparse.RawTextHelpFormatter)
    ARGUMENT_PARSER.add_argument('project_root',
                                 type=valid_dir,
                                 metavar='PROJECT_ROOT',
                                 help='Path to the root of the F@H project')
    ARGUMENT_PARSER.add_argument('mapper',
                                 type=valid_file,
                                 metavar='MAPPER',
                                 help='A .csv with the mapping values')
    ARGUMENT_PARSER.add_argument('--dry-run',
                                 action='store_true',
                                 default=False,
                                 help='Display verbose output' +
                                 '...without doing scary stuff. Promise.')
    ARGS = ARGUMENT_PARSER.parse_args()
    FAHDataRunNameConverter(ARGS.project_root,
                            ARGS.mapper,
                            ARGS.dry_run).__main__()
