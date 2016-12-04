#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import fnmatch
import subprocess
import itertools


def comment_tag(language):
    return '//'


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


def contents_of_annotated_file(filename, annotations):
    result = []
    with open(filename) as source_file:
        for line, annotation in itertools.izip(
                source_file, annotations):
            annotated_file_line = line

            if len(annotation) > 0:
                is_line_containing_comment = comment_tag(extension) in line
                comment_to_append = ('\t' + annotation) \
                    if is_line_containing_comment \
                    else '\t\t' + comment_tag(extension) + annotation
                annotated_file_line += comment_to_append + '\n'

            result.append(annotated_file_line)
    return result


def annotate_single_file(filename):
    author_annotations = git_blame_authors(filename)

    collate_annotations = annotate_only_first_line_of_block(author_annotations)

    return contents_of_annotated_file(filename, collate_annotations)

if __name__ == "__main__":
    directory = sys.argv[1]
    extension = sys.argv[2]
    os.chdir(directory)

    if not os.path.exists('collated'):
        os.mkdir('collated')

    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.' + extension):
            annotated_results = annotate_single_file(root + '/' + filename)

            collated_filename = 'collated/' + filename + '.annotated'
            with open(collated_filename, 'w+') as annotated_file:
                for line in annotated_results:
                    annotated_file.write(line)
