# -*- coding: utf-8 -*-
'''
Created on 2018-10-31

@author: zhengjin
'''

import getopt
import sys


def cmd_args_parse():
    opts, _ = getopt.getopt(sys.argv[1:], "hi:o:")

    if len(opts) == 0:
        usage()
        exit(0)
    
    input_file = ""
    output_file = ""
    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-h":
            usage()
            exit(0)
    print('input file: %s, output file: %s' % (input_file, output_file))


def usage():
    lines = []
    lines.append('usage:')
    lines.append('-i: input file')
    lines.append('-o: output file')
    lines.append('-h: help')
    print('\n'.join(lines))


if __name__ == '__main__':
    
    cmd_args_parse()
