# -*- coding:utf-8 -*-


# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/3/23
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014

import unittest
import os
from method_analysis_job import job_start
from method_analysis_utils.scanner import get_scanner,method_scanner
from file_utils import dir_scanner

class TestMethodAnalysis(unittest.TestCase):
    def test_getscanner(self):
        '''
        检测scanner实例对象是否得到
        :return:
        '''
        s = get_scanner()
        self.assertIsInstance(s,method_scanner,msg="扫描器对象构建失败")

    # @unittest.skip
    def test_morefiles(self):
        root_path = os.getcwd()
        dir_path = r"\source\code"
        file_list = dir_scanner(dir_path)
        for path in file_list:
            self.assertIsNotNone(job_start(path))


if __name__ == "__main__":
    unittest.main()



