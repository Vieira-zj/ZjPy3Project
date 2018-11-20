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
    Generate profile chart include CPU, Memory (Pss), Upflow, Downflow.
    '''

    CATEGORY_CPU = 0
    CATEGORY_MEM = 1
    CATEGORY_UPFLOW = 2
    CATEGORY_DOWNFLOW = 3

    __profile_type_list = ('cpu_com_jd_b2b.txt,cpuSystem.txt', 'pss_com_jd_b2b.txt,pssSystemLeft.txt', 'upflow_com_jd_b2b.txt', 'downflow_com_jd_b2b.txt')

    def __init__(self, logger, report_root_path, is_show=False):
        '''
        Constructor
        '''
        self.__logger = logger
        self.__is_show = is_show
        self.__report_root_path = report_root_path
        self.__handtest_dir_path = os.path.join(self.__report_root_path, 'handTest')
        self.sysutils = SysUtils(logger)
        
    # --------------------------------------------------------------
    # Read Profile Source Data
    # --------------------------------------------------------------
    def __read_profile_data(self, profile_types):
        y1_arr = []
        y2_arr = []
        if len(profile_types) == 1:
            y1_arr = self.sysutils.read_lines_from_file(self.__get_abs_profile_filepath(profile_types[0]))
        elif len(profile_types) == 2:
            y1_arr = self.sysutils.read_lines_from_file(self.__get_abs_profile_filepath(profile_types[0]))
            y2_arr = self.sysutils.read_lines_from_file(self.__get_abs_profile_filepath(profile_types[1]))
        else:
            raise Exception('Invalid profile type!')
        
        if len(y1_arr) == 0:
            raise Exception('y1_arr size is zero!')
        
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
    # Build Charts
    # --------------------------------------------------------------
    def build_chart(self, p_category):
        plt.title('APP Profile Test')
        plt.grid(True, color='green', linestyle='--', linewidth='1')
        
        profile_types = self.__profile_type_list[p_category].split(',')
        if p_category == self.CATEGORY_CPU:
            self.__build_cpu_chart(profile_types)
            self.__save_image('cpu')
        elif p_category == self.CATEGORY_MEM:
            self.__build_mem_pss_chart(profile_types)
            self.__save_image('mem')
        elif p_category == self.CATEGORY_UPFLOW:
            self.__build_upflow_chart(profile_types)
            self.__save_image('upflow')
        elif p_category == self.CATEGORY_DOWNFLOW:
            self.__build_downflow_chart(profile_types)
            self.__save_image('downflow')
        else:
            raise Exception('Invalid input profile type!')
    
        if self.__is_show:
            plt.show()
        plt.close('all')
    
    def __build_cpu_chart(self, profile_types):
        y1_arr, y2_arr = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y1_arr))]
        plt.plot(x_arr, y1_arr, color='red')
        plt.plot(x_arr, y2_arr, color='blue')

        x_label_desc1 = 'Red: %s, average: %.2f' % (profile_types[0].rstrip('.txt'), np.average(y1_arr))
        x_label_desc2 = 'Blue: %s, average: %.2f' % (profile_types[1].rstrip('.txt'), np.average(y2_arr))
        plt.xlabel('Time (secs)\n%s\n%s' % (x_label_desc1, x_label_desc2))
        plt.ylabel('CPU usage (%)')

    def __build_mem_pss_chart(self, profile_types):
        y1_arr, y2_arr = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y1_arr))]
        plt.plot(x_arr, y1_arr, color='red')
        plt.plot(x_arr, y2_arr, color='blue')
        
        x_label_desc1 = 'Red: %s, average: %.2f MB' % (profile_types[0].rstrip('.txt'), np.average(y1_arr))
        x_label_desc2 = 'Blue: %s, average: %.2f MB' % (profile_types[1].rstrip('.txt'), np.average(y2_arr))
        plt.xlabel('Time (secs)\n%s\n%s' % (x_label_desc1, x_label_desc2))
        plt.ylabel('Memory Pss Usage (MB)')
 
    def __build_upflow_chart(self, profile_types):
        y_arr, _ = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y_arr))]
        plt.plot(x_arr, y_arr, color='red')
        
        x_label_desc = '%s, average: %.2f KB' % (profile_types[0].rstrip('.txt'), np.average(y_arr))
        plt.xlabel('Time (secs)\n%s' % x_label_desc)
        plt.ylabel('Upflow (KB)')

    def __build_downflow_chart(self, profile_types):
        y_arr, _ = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y_arr))]
        plt.plot(x_arr, y_arr, color='red')
        
        x_label_desc = '%s, average: %.2f KB' % (profile_types[0].rstrip('.txt'), np.average(y_arr))
        plt.xlabel('Time (secs)\n%s' % x_label_desc)
        plt.ylabel('Downflow (KB)')

    def __save_image(self, key):
        save_dpi = 300
        save_path = os.path.join(self.__report_root_path, 'profile_%s.png' % key)
        plt.savefig(save_path, format='png', dpi=save_dpi)
        

if __name__ == '__main__':
    
    from monkeytest.constants import Constants
    from monkeytest.log_manager import LogManager

    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()

    root_path = r'D:\ZJWorkspaces\ZjPy3Project\MonkeyReports\18-11-19_202559'
    parser = ChartParser(logger, root_path)
    parser.build_chart(ChartParser.CATEGORY_CPU)
    parser.build_chart(ChartParser.CATEGORY_MEM)
    parser.build_chart(ChartParser.CATEGORY_UPFLOW)
    parser.build_chart(ChartParser.CATEGORY_DOWNFLOW)

    manager.clear_log_handles()
    print('chart parser test DONE.')
