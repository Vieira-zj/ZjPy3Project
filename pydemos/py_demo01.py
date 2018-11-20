# -*- coding: utf-8 -*-
'''
Created on 2018-10-31

@author: zhengjin
'''

import getopt
import sys


def cmd_args_parse():
    # "hi:o:": h => -h, i: => -i input_file, o: => -o output_file
    opts, _ = getopt.getopt(sys.argv[1:], 'hi:o:')

    if len(opts) == 0:
        usage()
        exit(0)
    
    input_file = ''
    output_file = ''
    for op, value in opts:
        if op == '-i':
            input_file = value
        elif op == '-o':
            output_file = value
        elif op == '-h':
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


def chart_demo():
    '''
    pre-conditions: 
    $ pip install numpy
    $ pip install matplotlib
    '''
    import numpy as np
    print('numpy version: ' + np.__version__)

    import matplotlib
    print('matplotlib version: ' + matplotlib.__version__)

    import matplotlib.pyplot as plt

    plt.title('Chart Test')
    plt.xlabel('X_label_text\n green: system_cpu, blue: user_cpu')
    plt.ylabel('Y_label_text')
    
    x_arr = [x for x in range(0, 10)]
    y_arr = [y for y in range(0, 20) if y % 2 == 0]
    z_arr = [y for y in range(0, 20) if y % 2 != 0]
    plt.plot(x_arr, y_arr, color='red')
    plt.plot(x_arr, z_arr, color='blue')
    plt.grid(True, color='green', linestyle='--', linewidth='1')
    plt.show()


if __name__ == '__main__':
    
#     cmd_args_parse()
    chart_demo()
