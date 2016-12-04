#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import itertools

if __name__ == "__main__":
    cwd = sys.argv[1]
    file = sys.argv[2]
    os.chdir(cwd)

    try:
        blame = 'git blame -w -M -C  --line-porcelain {}'.format(file).split()
        author_info = subprocess.Popen(blame, stdout=subprocess.PIPE,
                                       shell=True)
        sed_output = subprocess.Popen(["sed", "-n", "s/^author //p"],
                                      stdin=author_info.stdout,
                                      stdout=subprocess.PIPE)
        sort_output = subprocess.Popen(['sort'],
                                      stdin=sed_output.stdout,
                                      stdout=subprocess.PIPE)
        uniq_output = subprocess.Popen(['uniq', '-c'],
                                      stdin=sort_output.stdout,
                                      stdout=subprocess.PIPE)
        sortrn_output = subprocess.Popen(['sort', '-rn'],
                                      stdin=uniq_output.stdout,
                                      stdout=subprocess.PIPE)
        authors_loc = uniq_output.communicate()[0]

    except subprocess.CalledProcessError as e:
        print('unable to complete chain of git commands', file=sys.stderr)
        print(e, file=sys.stderr)
        raise e

    table = (line.strip() for line in authors_loc.split('\n'))

    for line in table:
        print(line)
