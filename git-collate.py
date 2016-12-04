#!/usr/bin/env python

import os
import sys
import subprocess
import itertools

commands = {
    'blame' : "git blame --line-porcelain {}",
    'sed' : ["sed", "-n", "s/^author //p"],
    'ls' : ['ls'],
}

if __name__ == "__main__":
    cwd = sys.argv[1]
    file = sys.argv[2]
    os.chdir(cwd)

    command_split = commands['blame'].format(file).split()

    try:
        author_info = subprocess.Popen(command_split, stdout=subprocess.PIPE, shell=True) #cwd=r'C:/Users/user/SchoolLifeSimulator')
        sed_output = subprocess.Popen(commands['sed'], stdin=author_info.stdout, stdout=subprocess.PIPE)
        author_annotations = sed_output.communicate()[0].split("\n")
    except subprocess.CalledProcessError as e :
        print e

    with open('src/main/java/com/officelife/Main.java') as source_file:
        for line, annotation in itertools.izip(source_file, author_annotations):
            print line.rstrip() + '\t\t//' + annotation  # todo determine comment from language, ignore empty lines
