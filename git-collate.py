#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import itertools

commands = {
    'blame': 'git blame -w -M -C --line-porcelain {}',
    'sed': ["sed", "-n", "s/^author //p"],
}

if __name__ == "__main__":
    cwd = sys.argv[1]
    file = sys.argv[2]
    os.chdir(cwd)

    try:
        blame = commands['blame'].format(file).split()
        author_info = subprocess.Popen(blame, stdout=subprocess.PIPE,
                                       shell=True)
        sed_output = subprocess.Popen(commands['sed'],
                                      stdin=author_info.stdout,
                                      stdout=subprocess.PIPE)
        author_annotations = sed_output.communicate()[0].split("\n")
    except subprocess.CalledProcessError as e:
        print(e, file=sys.stderr)
        raise e

    collate_annotations = []
    previous = ''
    for author in author_annotations:
        if author != previous:
            collate_annotations.append('@@author ' + author)
        else:
            collate_annotations.append('')
        previous = author

    with open(file) as source_file:
        for line, annotation in itertools.izip(
                source_file, collate_annotations):
            if len(annotation) == 0:
                print(line)
            else:
                # todo determine comment from language, ignore empty lines
                print(line.rstrip() + '\t\t//' + annotation)
