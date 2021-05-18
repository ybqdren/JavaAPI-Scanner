# -*- coding:utf-8 -*-


# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/3/24
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014

import unittest
from file_utils import dir_scanner
import os

class TestFile(unittest.TestCase):
    def test_dirallfile_one(self):
        '''
        测试目录+文件这种 目录下没有目录
        :return:
        '''
        root_path = os.getcwd()
        path = r"\source\code"
        # path = r"E:\ZHAOWEN\RESPONSE\race\team-1186152014\api-scanner\source"
        self.assertIsNotNone(dir_scanner(path))

    def test_dirallfile_more(self):
        '''
        测试目录+文件/目录这种 目录下面还有目录
        :return:
        '''
        root_path = os.getcwd()
        path = root_path+r"\source"
        file_list = dir_scanner(path)
        print(file_list)
        self.assertIsNotNone(file_list)

    @unittest.skip
    def test_dirallfile_file(self):
        '''
        测试路径指向一个文件
        :return:
        '''
        root_path = os.getcwd()
        path = root_path + r"\source\code\J_1.java"
        file_list = dir_scanner(path)
        # print(file_list)
        self.assertIsNotNone(file_list)

    @unittest.skip
    def test_outputpath(self):
        '''
        测试输出分析文件地址
        :return:
        '''
        output_path = r""

    def test_path(self):
        '''
        路径测试
        :return:
        '''
        print(os.getcwd())

if __name__ == "__main__":
    unittest.main()