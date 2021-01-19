# coding: utf-8

import time
import os
import traceback
from shutil import copyfile


def get_current_date_and_time():
    return time.strftime('%y-%m-%d_%H%M%S')


def list_ods_files(dir_path):
    matched = []
    for f in os.listdir(dir_path):
        suffix = os.path.splitext(f)[1]
        if suffix == '.ods':  # 只匹配后缀为 ods 的文件
            matched.append(f)
    return matched


def get_rename_entries(files, src_version, new_version):
    rename_entries = []  # (旧文件名，新文件名)
    for f in files:
        items = f.split('_')
        tmps = []
        for item in items:
            if item == src_version:
                tmps.append(new_version)
            else:
                tmps.append(item)
        rename_entries.append((f, '_'.join(tmps)))
    return rename_entries


def main(dir_path, src_version, new_version):
    '''
    批量文件版本号更新。
    '''
    matched = list_ods_files(dir_path)
    if len(matched) == 0:
        print('error: no ods files found in dir:', dir_path)
        return
    print('reversion files count:', len(matched))

    copied_dir_path = dir_path + '_copied_' + get_current_date_and_time()
    if os.path.exists(copied_dir_path):
        print('error: copied dir already exist:', copied_dir_path)
        return

    os.mkdir(copied_dir_path)
    rename_entries = get_rename_entries(matched, src_version, new_version)
    for entry in rename_entries:
        old_name = entry[0]
        new_name = entry[1]
        print('file reversion:', old_name, new_name)
        try:
            copyfile(os.path.join(dir_path, old_name),
                     os.path.join(copied_dir_path, new_name))
        except IOError as e:
            print('copy failed:', old_name, new_name)
            print('error:', e)
        except:
            print("unexpected error:", traceback.print_stack())


if __name__ == '__main__':

    dir_path = '/Users/jinzheng/Downloads/data_files'
    src_version = '20.12.0.0'
    new_version = '20.13.1.1'
    main(dir_path, src_version, new_version)
    print('files reversion finished.')
