#!/usr/bin/env python

import os
import subprocess
import itertools

blame = "git blame --line-porcelain {}"
sed = ["sed", "-n", "s/^author //p"]
ls = ['ls']

os.chdir('C:/Users/user/SchoolLifeSimulator')

command_split = blame.format('src/main/java/com/officelife/Main.java').split()

try:
	author_info = subprocess.Popen(command_split, stdout=subprocess.PIPE, shell=True) #cwd=r'C:/Users/user/SchoolLifeSimulator')
	sed_output = subprocess.Popen(sed, stdin=author_info.stdout, stdout=subprocess.PIPE)
	author_annotations = sed_output.communicate()[0].split("\n")
except subprocess.CalledProcessError as e :
	print e

with open('src/main/java/com/officelife/Main.java') as source_file:
	for line, annotation in itertools.izip(source_file, author_annotations):
		print line.rstrip() + '\t\t//' + annotation	 # todo determine comment from language, ignore empty lines

