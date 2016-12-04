#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import fnmatch
import subprocess
import itertools

def comment_tag(language):
    return '//';

def annotate_single_file(filename):
    try:
        blame = 'git blame -w -M -C --line-porcelain {}'.format(filename).split()

        author_info = subprocess.Popen(blame, stdout=subprocess.PIPE,
                                       shell=True)
        sed_output = subprocess.Popen(["sed", "-n", "s/^author //p"],
                                      stdin=author_info.stdout,
                                      stdout=subprocess.PIPE)
        author_annotations = sed_output.communicate()[0].split("\n")
    except subprocess.CalledProcessError as e:
        print(e, file=sys.stderr)
        raise e

    collate_annotations = []
    previous = ''
    for author in author_annotations:
        collate_annotations.append(('@@author ' + author) if author != previous else '')
        previous = author
    
    result = []
    with open(filename) as source_file:
        for line, annotation in itertools.izip(
                source_file, collate_annotations):
            if len(annotation) == 0:
                result.append(line)
            else:
                # todo determine comment from language, ignore empty lines
                result.append(line.rstrip() + '\t\t' + comment_tag(extension) + annotation)

    return result

if __name__ == "__main__":
    directory = sys.argv[1]
    extension = sys.argv[2]
    os.chdir(directory)

    if not os.path.exists('collated'):
        os.mkdir('collated')

    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.' + extension):
            annotated_results = annotate_single_file(root + '\\' + filename)

            with open('collated/' + filename + '.annotated', 'w+') as annotated_file:
                for line in annotated_results:
                    annotated_file.write(line + '\n')
