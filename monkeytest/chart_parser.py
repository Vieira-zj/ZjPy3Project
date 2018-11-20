# -*- coding: utf-8 -*-
'''
Created on 2018-11-20

@author: zhengjin
'''

import os
import matplotlib.pyplot as plt
import numpy as np
from monkeytest.sys_utils import SysUtils


class ChartParser(object):
    '''
    classdocs
    '''

    PROFILE_TYPE_CPU = 0
    PROFILE_TYPE_MEM = 1
    PROFILE_TYPE_UPFLOW = 2
    PROFILE_TYPE_DOWNFLOW = 3

    __profile_type_list = ('cpu_com_jd_b2b.txt,cpuSystem.txt', 'pss_com_jd_b2b.txt,pssSystemLeft.txt', 'upflow_com_jd_b2b.txt', 'downflow_com_jd_b2b.txt')

    def __init__(self, logger, report_root_path):
        '''
        Constructor
        '''
        self.__logger = logger
        self.__report_root_path = report_root_path
        self.__handtest_dir_path = os.path.join(self.__report_root_path, 'handTest')
        self.__profile_types = self.__profile_type_list[0].split(',')  # default cpu
        self.sysutils = SysUtils(logger)
        
    # --------------------------------------------------------------
    # Read Profile Source Data
    # --------------------------------------------------------------
    def __read_profile_data(self, p_type):
        profile_types = self.__profile_type_list[p_type].split(',')
        
        y1_arr = []
        y2_arr = []
        if len(profile_types) == 1:
            y1_arr = self.sysutils.read_lines_from_file(self.__get_abs_profile_filepath(profile_types[0]))
        elif len(profile_types) == 2:
            y1_arr = self.sysutils.read_lines_from_file(self.__get_abs_profile_filepath(profile_types[0]))
            y2_arr = self.sysutils.read_lines_from_file(self.__get_abs_profile_filepath(profile_types[1]))
        else:
            raise Exception('Invalid profile type!')
        
        ret_y1_arr = [int(float(item.split()[1])) for item in y1_arr]
        ret_y2_arr = []
        if len(y2_arr) > 0:
            ret_y2_arr = [int(float(item.split()[1])) for item in y2_arr]
        
        return self.__fix_negative_num_issue(ret_y1_arr), self.__fix_negative_num_issue(ret_y2_arr)

    def __get_abs_profile_filepath(self, file_name):
        return os.path.join(self.__handtest_dir_path, file_name)

    def __fix_negative_num_issue(self, arr):
        for i in range(0, len(arr)):
            if arr[i] < 0:
                arr[i] = 0
        return arr
    
    # --------------------------------------------------------------
    # Generate Chart
    # --------------------------------------------------------------
    def generate_chart(self, p_type):
        if p_type == self.PROFILE_TYPE_CPU:
            self.__generate_cpu_chart(p_type)
        elif p_type == self.PROFILE_TYPE_MEM:
            self.__generate_mem_pss_chart(p_type)
        else:
            raise Exception('Invalid input profile type!')
    
        plt.title('APP Profile Test')
        plt.grid(True, color='green', linestyle='--', linewidth='1')
        plt.show()
        
    def __generate_cpu_chart(self, p_type):
        y1_arr, y2_arr = self.__read_profile_data(p_type)
        
        x_label_desc1 = 'Red: %s, average: %.2f' % (self.__profile_types[0].rstrip('.txt'), np.average(y1_arr))
        x_label_desc2 = 'Blue: %s, average: %.2f' % (self.__profile_types[1].rstrip('.txt'), np.average(y2_arr))
        plt.xlabel('Time (secs)\n%s\n%s' % (x_label_desc1, x_label_desc2))
        plt.ylabel('MEM usage (%)')
 
        x_arr = [x for x in range(0, len(y1_arr))]
        plt.plot(x_arr, y1_arr, color='red')
        plt.plot(x_arr, y2_arr, color='blue')
 
    def __generate_mem_pss_chart(self, p_type):
        y1_arr, y2_arr = self.__read_profile_data(p_type)

        x_label_desc1 = 'Red: %s, average: %.2f MB' % (self.__profile_types[0].rstrip('.txt'), np.average(y1_arr))
        x_label_desc2 = 'Blue: %s, average: %.2f MB' % (self.__profile_types[1].rstrip('.txt'), np.average(y2_arr))
        plt.xlabel('Time (secs)\n%s\n%s' % (x_label_desc1, x_label_desc2))
        plt.ylabel('Memory Pss Usage (MB)')
 
        x_arr = [x for x in range(0, len(y1_arr))]
        plt.plot(x_arr, y1_arr, color='red')
        plt.plot(x_arr, y2_arr, color='blue')
        
        
if __name__ == '__main__':
    
    from monkeytest.constants import Constants
    from monkeytest.log_manager import LogManager

    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()

    root_path = r'D:\ZJWorkspaces\ZjPy3Project\MonkeyReports\18-11-19_202559'
    parser = ChartParser(logger, root_path)
#     parser.generate_chart(ChartParser.PROFILE_TYPE_CPU)
    parser.generate_chart(ChartParser.PROFILE_TYPE_MEM)

    manager.clear_log_handles()
    print('chart parser test DONE.')
