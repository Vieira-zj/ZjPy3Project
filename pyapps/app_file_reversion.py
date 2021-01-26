# coding: utf-8

import time
import os
import traceback
from shutil import copyfile


def get_current_date_and_time():
    return time.strftime('%y-%m-%d_%H%M%S')


def list_ods_files(dir_path, match_suffix='.java'):
    '''
    match_suffix 只匹配指定后缀的文件
    '''
    matched = []
    not_matched = []
    for f in os.listdir(dir_path):
        suffix = os.path.splitext(f)[1]
        if suffix == match_suffix:
            matched.append(f)
        else:
            not_matched.append(f)
    return matched, not_matched


def get_rename_entries_by_split(file_names, src_version, new_version):
    files_to_rename = []
    files_not_match_ver = []
    for f in file_names:
        if src_version in f:
            files_to_rename.append(f)
        else:
            files_not_match_ver.append(f)

    rename_entries = []  # (旧文件名，新文件名)
    for f in files_to_rename:
        items = f.split('_')
        tmps = []
        for item in items:
            if item == src_version:
                tmps.append(new_version)
            else:
                tmps.append(item)
        rename_entries.append((f, '_'.join(tmps)))
    return rename_entries, files_not_match_ver


def get_rename_entries_by_replace(file_names, src_version, new_version):
    files_not_match_ver = []
    rename_entries = []  # (旧文件名，新文件名)

    for f_name in file_names:
        if src_version in f_name:
            new_file_name = f_name.replace(src_version, new_version)
            rename_entries.append((f_name, new_file_name))
        else:
            files_not_match_ver.append(f_name)

    return rename_entries, files_not_match_ver


def reversion_by_copy(src_dir_path, rename_entries):
    copied_dir_path = src_dir_path + '_copied_' + get_current_date_and_time()
    if os.path.exists(copied_dir_path):
        print('error: copied dir already exist:', copied_dir_path)
        return

    os.mkdir(copied_dir_path)
    for entry in rename_entries:
        src_name = entry[0]
        dst_name = entry[1]
        print('file reversion by copy: [%s] to [%s]' % (src_name, dst_name))
        try:
            copyfile(os.path.join(src_dir_path, src_name),
                     os.path.join(copied_dir_path, dst_name))
        except IOError as e:
            print('copy failed: [%s] to [%s]' % (src_name, dst_name))
            print('error:', e)
        except:
            print('unexpected error:', traceback.print_stack())


def reversion_by_move(src_dir_path, rename_entries):
    for entry in rename_entries:
        src_name = entry[0]
        dst_name = entry[1]
        print('file reversion: [%s] to [%s]' % (src_name, dst_name))

        src_path = os.path.join(src_dir_path, src_name)
        dst_path = os.path.join(src_dir_path, dst_name)
        try:
            os.rename(src_path, dst_path)
        except IOError as e:
            print('move failed: [%s] to [%s]' % (src_name, dst_name))
            print('error:', e)
        except:
            print('unexpected error:', traceback.print_stack())


def print_invalid_entries(not_matched, files_not_match_ver):
    if len(not_matched) > 0:
        print('files not .ods suffix:', not_matched)
    if len(files_not_match_ver) > 0:
        print('files not matched version:', files_not_match_ver)


def main(dir_path, src_version, new_version, is_copy=False):
    '''
    批量文件版本号更新。
    '''
    matched, not_matched = list_ods_files(dir_path)
    if len(matched) == 0:
        print('error: no ods files found in dir:', dir_path)
        return
    print('reversion files count:', len(matched))

    rename_entries, files_not_match_ver = get_rename_entries_by_replace(
        matched, src_version, new_version)
    if len(rename_entries) == 0:
        print('no matched files found.')
        print_invalid_entries(not_matched, files_not_match_ver)
        return

    if is_copy:
        reversion_by_copy(dir_path, rename_entries)
    else:
        reversion_by_move(dir_path, rename_entries)
    print_invalid_entries(not_matched, files_not_match_ver)


if __name__ == '__main__':

    dir_path = '/Users/jinzheng/Downloads/data_files'
    src_version = '21_2_1_3'
    new_version = '21_2_1_6'
    main(dir_path, src_version, new_version)
    print('files reversion finished.')
