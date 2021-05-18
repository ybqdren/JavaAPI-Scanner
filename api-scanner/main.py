# -*- coding:utf-8 -*-


# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/3/23
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014

from method_analysis_job import job_start
import logging.config
from file_utils import  dir_scanner,file_write
from method_analysis_job import job_start
import os
import time

# 配置日志
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def start_init():
    '''
    初始化控制台显示信息
    :return:
    '''
    print("===============Java API 提取器==============")
    time.sleep(0.5)
    print("----------------------------------------")
    print("|  队伍名称：mymk_one(1186152014)      |")
    print("|  主要成员：赵雯<withzhaowen@126.com> |")
    print("|  版本信息：v1.0                      |")
    print("----------------------------------------")
    print("\n")
    time.sleep(1)


if __name__ == "__main__":
    out_path = ""
    i = 1

    # 控制台初始化
    start_init()

    while True:
        print("请设置输入路径（输入后请回车，如果要退出请输入exit）")
        dir_path = input("-- > ")
        file_list = dir_scanner(dir_path)

        for file in file_list:
            logger.info("> 正在解析第" + str(i) + "个文件......")
            info_list, public_list, unpublic_list, isClass= job_start(file)
            if isClass:
                logger.info("> 正在写入中......")
                if file_write(out_path, info_list, public_list, unpublic_list):
                    logger.info("> 第" + str(i) + "个文件写入成功")
                else:
                    logger.info("> 第" + str(i) + "个文件写入失败")
            else:
                logger.info("> 不是一个可以提取的文件")
            i += 1
        logging.info("操作完毕")

        if dir_path == "exit":
            break

    print("bye~ ")