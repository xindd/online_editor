#!/usr/bin/env python
# coding: utf-8


import nbformat as nbf
import os
import sys, getopt

from nbconvert.preprocessors import ExecutePreprocessor

opts, args = getopt.getopt(sys.argv[1:], 'i:o:s:', ['input_file=', 'output_file=', 'script_version='])
input_file = ''
output_file = ''
script_version = ''
for op, value in opts:
    if op == "-i" or op == 'input_file':
        input_file = value
    elif op == "-o" or op == 'output_file':
        output_file = value
    elif op == "-s" or op == 'script_version':
        script_version = value
    else:
        print('arg error...')
        sys.exit()



# input_file = 'print(123)'
# script_version = 'Python-3.6.5' # 'R-3.4.4'
# output_file = 'test'

meta_data = nbf.read(fp = script_version+'.ipynb', as_version=4)
try:
    with open(input_file, 'r') as f:
        res_list = []
        for line in f.readlines():
            res_list.append(line)
        meta_data.cells[0].source = res_list
except IOError:
    print('IOError')
    sys.exit()

nbf.write(meta_data, output_file+'.ipynb')


res = os.system('jupyter nbconvert --execute --no-input --allow-error --to html --template basic '+ output_file + '.ipynb')
if res == 0:
    print('success')
else:
    print('failed')





