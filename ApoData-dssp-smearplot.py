#!/usr/bin/env python

import os
import re
import subprocess

CWD = os.getcwd()
PROT_RES = 0
if "1LS4" in CWD:
    PROT_RES = 162
elif "2KC3" in CWD:
    PROT_RES = 182
else:
    PROT_RES = 298
LAGTIME = 0
GREP_LINE = subprocess.Popen(('grep', '{}'.format(CWD),
                              '/data/APO-data/scripts/lag-time.txt'), stdout=subprocess.PIPE)
LAGTIME = int(subprocess.check_output(('awk', '{print $2}'),
                                      stdin=GREP_LINE.stdout).rstrip()) / 100
CWD_WALK = os.walk(CWD)
XPM_DATA = []
for directory, _, _ in CWD_WALK:
    directory_search = re.search('(?<=/0)\d+', directory)
    if directory_search is not None:
        xpm = open('{}/ss.xpm'.format(directory), mode='r')
        xpm_lines = xpm.readlines()
        xpm_lines_subset = xpm_lines[
            (len(xpm_lines) - PROT_RES):len(xpm_lines)]
        XPM_DATA.append(xpm_lines_subset)
REF_COUNT = len(XPM_DATA[0])
prob = []
for subset in XPM_DATA:
    assert len(subset) == REF_COUNT, 'Inconsistent number of residues.'
    h = []
    t = []
    c = []
    b = []
    for residue_index in xrange(len(subset)):
        h.append(subset[residue_index].count('H', 1, len(subset[residue_index]) - 3) + subset[residue_index].count('G', 1, len(subset[residue_index]) - 3) + subset[residue_index].count('I', 1, len(subset[residue_index]) - 3))
        t.append(subset[residue_index].count('S', 1, len(subset[residue_index]) - 3) + subset[residue_index].count('T', 1, len(subset[residue_index]) - 3))
        c.append(subset[residue_index].count('~', 1, len(subset[residue_index]) - 3))
        b.append(subset[residue_index].count('B', 1, len(subset[residue_index]) - 3) + subset[residue_index].count('E', 1, len(subset[residue_index]) - 3))
    subset_matrix = [h, t, c, b]
    prob.append(subset_matrix)
        