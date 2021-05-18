# -*- coding:utf-8 -*-

# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/3/23
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014
# 方法头解析器

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


def get_complier():
    m_complier = method_complier.get_instance()
    return m_complier

class method_complier():
    mstr_line = ""

    def complier_start(self):
        logger.info("==================Code Complier Start==================")

    def complier_method(self,mstr_line):
        '''
        编译器
        :param mstr_line: 待编译的方法
        :return: 一个布尔值，用于判定是否为外部可访问API True|False
        '''
        if mstr_line.startswith("public"):
            return True
        else:
            return False

    def complier_close(self):
        logger.info("==================Code Complier End==================")

    @classmethod
    def get_instance(cls):
        '''
        获取一个complier实例对象
        :type @classmethod
        :return: 一个methode_complier类实例对象
        '''
        return method_complier()

