# -*- coding: utf-8 -*-
'''
Created on 2019-03-07

@author: zhengjin
'''

import os
import sys
import glob
import smtplib
import zipfile

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.append('../../')
from utils import Constants
from utils import LogManager
from apitest.common import LoadConfigs


class EmailsHelper(object):

    __helper = None

    @classmethod
    def get_intance(cls):
        if cls.__helper is None:
            logger = LogManager.get_instance().get_logger()
            configs = LoadConfigs.all_configs
            cls.__helper = EmailsHelper(logger, configs)
        return cls.__helper

    def __init__(self, logger, configs):
        self.__logger = logger
        self.__configs = configs.get(LoadConfigs.SECTION_EMAIL)
        self.__msg = MIMEMultipart('mixed')
        self.__attach_files_dir = ''

    def set_attached_files_dir(self, dir_path):
        self.__attach_files_dir = dir_path
        return self

    def __config_header(self):
        self.__msg['subject'] = self.__configs.get('subject')
        self.__msg['from'] = self.__configs.get('sender')
        self.__msg['to'] = self.__configs.get('receivers')

    def __config_content(self):
        content_plain = MIMEText(self.__configs.get('content'), 'plain', 'utf-8')
        self.__msg.attach(content_plain)

    def __config_attach_file(self):
        if len(self.__attach_files_dir) == 0:
            return
        if not os.path.exists(self.__attach_files_dir):
            self.__logger.warn('dir is not exist: ' + self.__attach_files_dir)
            return

        zip_file_name = 'test_results.zip'
        zip_path = os.path.join(self.__attach_files_dir, zip_file_name)
        zip_input = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        try:
            files = glob.glob(self.__attach_files_dir + '/*')
            for file in files:
                zip_input.write(file)
        finally:
            if zip_input is not None:
                zip_input.close()

        attach_file = MIMEText(open(zip_path, 'rb').read(), 'base64', 'utf-8')
        attach_file['Content-Type'] = 'application/octet-stream'
        attach_file['Content-Disposition'] = 'attachment; filename="%s"' % zip_file_name
        self.__msg.attach(attach_file)

    def __create_smtp(self):
        smtp = smtplib.SMTP()

        host = self.__configs.get('mail_host')
        smtp.connect(host)

        user = self.__configs.get('mail_user')
        pwd = self.__configs.get('mail_pwd')
        smtp.login(user, pwd)

        return stmp

    def send_email(self):
        self.__config_header()
        self.__config_content()
        self.__config_attach_file()

        smtp = _create_smtp()
        try:
            from_addr = self.__configs.get('sender')
            to_addr = self.__configs.get('receivers').split(',')
            smtp.sendmail(from_addr, to_addr, self.__msg.as_string())
        finally:
            if smtp is not None:
                smtp.quit()

        self.__logger.info('Test report has been send by email.')


if __name__ == '__main__':

    # init
    log_manager = LogManager.get_instance(Constants.LOG_FILE_PATH)
    cfg_file_path = os.path.join(os.path.dirname(os.getcwd()), 'configs.ini')
    LoadConfigs.load_configs(cfg_file_path)

    emails = EmailsHelper.get_intance()
    emails.send_email()

    # dir_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/test_results')
    # emails.set_attached_files_dir(dir_path).send_email()

    log_manager.clear_log_handles()
    print('emails helper test DONE.')
