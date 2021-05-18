# -*- coding:utf-8 -*-


# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/3/24
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014
# 文件处理模块

import os
import logging.config
import json
import time

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


def dir_scanner(path):
    '''
    路径扫描器：遍历指定目录下的所有文件
    :param path: 指定的路径
    :return: 文件集合
    '''
    file_list = list()

    if os.path.isdir(path):
        for root,dirs,files in os.walk(path):
            for file in files:
                file_path = root+"\\"+file
                logging.info("获取到文件："+file)
                file_list.append(file_path)
    elif os.path.isfile(path):
        logger.info("传入路径为一个文件，获取到这个文件的路径："+path)
        file_list.append(path)

    return file_list


def file_write(out_path,info_list,public_list,unpublic_list):
    '''
    文件写出
    :param out_path 写出文件路径
    :param info_list: 方法信息 包 类
    :param public_list: 外部可访问API
    :param unpublic_list:  内部才能访问的API
    :return:

    json文件格式设定：
    {
        "info":
        {
            "package":[package],
            "class":[class]
        },
        "method":{
            "public":[
                [method],
                [method],
                [.....]
            ],
            "unpublic":[
                [method],
                [method],
                [.....]
            ]
        }
    }
    '''
    # ['方法信息', 'com.alibaba.fastjson', 'public abstract class JSON implements JSONStreamAware, JSONAware']
    # 封装构造json对象所要使用到的数据
    method_list = {"public":public_list,"unpublic":unpublic_list}
    method_info = {"package":info_list[0],"class":info_list[1]}
    method_json = {
        "info":method_info,
        "method":method_list
    }

    # 设定默认输出目录
    root_path = os.getcwd()
    temp_dir = root_path+"\\temp\\"

    # 检验传入的输出路径是否为一个目录
    if os.path.isdir(out_path):
        temp_dir = out_path

    # 设定文件名
    filename = method_info["class"]

    if filename == "":
        filename = int(round(time.time() * 1000))

    write_path = temp_dir+str(filename)+".json"
    logging.info("写出路径为："+write_path)

    # 写出文件
    with open(write_path,"w",encoding="utf-8") as file_object:
        try:
            file_object.write(json.dumps(method_json,ensure_ascii=False))
        except IOError as e:
            logging.info(str(type(e))+"......"+str(e.args))
            return False

    return True
