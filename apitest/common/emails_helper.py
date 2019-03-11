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

sys.path.append(os.getenv('PYPATH'))
from utils import Constants
from utils import LogManager
from utils import SysUtils
from apitest.common import LoadConfigs


class EmailsHelper(object):

    __emails = None

    @classmethod
    def get_intance(cls):
        if cls.__emails is None:
            cls.__emails = EmailsHelper()
        return cls.__emails

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__sysutils = SysUtils.get_instance()
        self.__configs = LoadConfigs.all_configs.get(LoadConfigs.SECTION_EMAIL)

        self.__msg = MIMEMultipart('mixed')
        self.__content_text = 'Default mail template from API test.'

    def set_content_text(self, text):
        self.__content_text = text
        return self

    def __build_mail_header(self):
        receivers = self.__configs.get('receivers').split(',')

        self.__msg['subject'] = self.__configs.get('subject')
        self.__msg['from'] = self.__configs.get('sender')
        self.__msg['to'] = ';'.join(receivers)
        self.__msg['date'] = self.__sysutils.get_current_date_with_sep()

    def __build_mail_content(self):
        content_plain = MIMEText(self.__content_text, 'plain', 'utf-8')
        self.__msg.attach(content_plain)

    def __attach_archive_file(self):
        dir_path = self.__configs.get('attachment')
        if len(dir_path) == 0:
            self.__logger.info('attachment dir is null, and skipped.')
            return
        if not os.path.exists(dir_path):
            self.__logger.error('attachment dir is not exist: ' + dir_path)
            return

        zip_file_name = 'test_results_%s.zip' % self.__sysutils.get_current_date_and_time()
        zip_path = os.path.join(dir_path, zip_file_name)
        zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        try:
            files = glob.glob(dir_path + '/*')
            for file in files:
                zip_file.write(file)
        finally:
            if zip_file is not None:
                zip_file.close()

        archive = MIMEText(open(zip_path, 'rb').read(), 'base64', 'utf-8')
        archive['Content-Type'] = 'application/octet-stream'
        archive['Content-Disposition'] = 'attachment; filename="%s"' % zip_file_name
        self.__msg.attach(archive)

    def __create_smtp(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.__configs.get('mail_host'))
        smtp.login(self.__configs.get('mail_user'), self.__configs.get('mail_pwd'))
        return smtp

    def send_email(self):
        self.__build_mail_header()
        self.__build_mail_content()
        self.__attach_archive_file()

        smtp = self.__create_smtp()
        from_addr = self.__configs.get('sender')
        to_addr = self.__configs.get('receivers').split(',')
        try:
            smtp.sendmail(from_addr, to_addr, self.__msg.as_string())
        finally:
            if smtp is not None:
                smtp.quit()

        self.__logger.info('Test reports email has been send.')


if __name__ == '__main__':

    # init logs and configs
    LogManager.build_logger(Constants.LOG_FILE_PATH)
    cfg_file_path = os.path.join(os.path.dirname(os.getcwd()), 'configs.ini')
    LoadConfigs.load_configs(cfg_file_path)

    mail_content = 'API test done.\nPlease read details of results in attachment.'
    mail = EmailsHelper.get_intance()
    mail.set_content_text(mail_content).send_email()

    LogManager.clear_log_handles()
    print('emails helper test DONE.')
