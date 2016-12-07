#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import fnmatch
import subprocess
import itertools


def comment_tag(language):
    return '//'

def tracked_files():
    command = 'git ls-tree -r master --name-only'.split()
    return subprocess.Popen(command, stdout=subprocess.PIPE) \
                        .communicate()[0].split()



def git_blame_authors(filename):
    try:
        blame = 'git blame -w -M -C --line-porcelain {}'.format(filename) \
            .split()

        author_info = subprocess.Popen(blame, stdout=subprocess.PIPE)

        sed_output = subprocess.Popen(["sed", "-n", "s/^author //p"],
                                      stdin=author_info.stdout,
                                      stdout=subprocess.PIPE)
        author_annotations = sed_output.communicate()[0].split("\n")
    except subprocess.CalledProcessError as e:
        print(e, file=sys.stderr)
        raise e
    return author_annotations


def annotate_only_first_line_of_block(author_annotations):

    collate_annotations = []
    previous = ''
    for author in author_annotations:
        collate_annotations.append(
            ('@@author ' + author) if author != previous else '')
        previous = author
    return collate_annotations


def contents_of_annotated_file(filename, annotations, extension):
    result = []
    with open(filename) as source_file:
        for line, annotation in itertools.izip(source_file, annotations):
            if len(annotation) > 0:
                result.append(comment_tag(extension) + annotation + '\n')

            result.append(line + '\n')

    return result


def annotate_single_file(filename, extension):
    author_annotations = git_blame_authors(filename)

    collate_annotations = annotate_only_first_line_of_block(author_annotations)

    return contents_of_annotated_file(filename, collate_annotations, extension)


def collate(args=None):
    extension = sys.argv[1]

    collate_dir = 'collated'
    if not os.path.exists(collate_dir):
        os.mkdir(collate_dir)

    filenames = tracked_files()
    for filename in fnmatch.filter(filenames, '*.' + extension):
        annotated_results = annotate_single_file(
            filename, extension)

        collated_filename = collate_dir + '/' + filename.split('/')[-1] + '.annotated'
        with open(collated_filename, 'w+') as annotated_file:
            for line in annotated_results:
                annotated_file.write(line)

if __name__ == "__main__":
    collate()
