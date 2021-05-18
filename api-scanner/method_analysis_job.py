# -*- coding:utf-8 -*-


# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/1/2
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014

from method_analysis_utils.scanner import get_scanner,token_type
import os
import logging.config
from method_analysis_utils.complier import get_complier

# 配置日志
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def comfig_complier():
    '''
    装配complier
    :return: 返回一个配置好的解析器
    '''
    c = get_complier()
    return c

def config_scanner():
    '''
    装配scanner
    :return: a value named s,type is scanner 返回一个配置好的扫描器
    '''
    s = get_scanner()

    # 初始化对象
    s.method_list = []
    s.left_single = 0
    s.right_single = 0

    # 1.方法名 method_name_token [a-zA-Z]+（虽然方法有诸如大驼峰 小驼峰之类的命名规范 但是有可能会有意外）
    # 2.方法参数 param_token ^[(][a-zA-Z0-9.png$\s,<A-Z>]+[)] -> (Properties prop1,Properties prop2)
    # 3.返回值类型 return_type_token 基本数据类型|自定义对象或者原生的对象|集合|void|泛型  （最简单的方法头一定都会标注返回类型)
    # 4.方法花括号 end_token { -> 方法头结束的标志 也是判别一行是否为方法的重要标识
    # 判断是否为为访问控制标识符
    access_token = token_type("access_token","default|public|protected|private")

    # 判断是否为关键字
    key_token = token_type("key_token","final|abstract|static|synchronized")

    # 判断是否还有下一行
    next_token = token_type("next_token","[//]+")

    # 判断是否为下一行类别的方法
    next_method_token = token_type("next_method_token","([a-zA-Z]+)\).*{")

    # 判断是否为必要token
    imp_token = token_type("imp_token","(.*)([a-zA-Z]+)(\s){0,}(\(.*\))[a-zA-Z\s]{0,}{")

    # 判断是否为无关字符使用代码即可完成 无需再使用正则
    invalid_token = token_type("invalid_token",".*")

    # 判断是否为接口
    interface_token = token_type("interface_token","\s(interface)\s|\s(@interface)\s")

    # 是否为类
    class_token = token_type("class_token","(class)\s(.*){(.*)")

    # 是否为包信息
    package_token = token_type("package_token","^package")

    # 是否为{
    left_single_token = token_type("left_single_token","(.*){(.*)")

    # 是否为}
    right_single_token = token_type("right_Single_token","(.*)}(.*)")

    # {} 同时存在
    all_single_token = token_type("all_single_token","(.*)}(.*){(.*)")

    token_type_dict = {"access_token":access_token,
                       "key_token":key_token,
                       "next_token":next_token,
                       "next_method_token":next_method_token,
                       "imp_token":imp_token,
                       "invalid_token":invalid_token,
                       "interface_token":interface_token,
                       "class_token":class_token,
                       "package_token":package_token,
                       "left_single_token":left_single_token,
                       "right_single_token":right_single_token,
                       "all_single_token":all_single_token
                       }

    s.set_token_type(token_type_dict)

    return s

def job_start(path):
    '''
    API分析工具开始入口
    :return: 外部可访问API与外部不可访问API集合
    '''

    s = config_scanner()
    isClass = False

    ###### 开始扫描源代码 #######
    s.read_file(path)

    method_list = s.find_method()

    # 判断method_list.pop(-1)为True还是False
    if method_list.pop(-1):
        isClass = True
        for m in method_list:
            logging.info(m)
        logger.info("总共提取到：(" + str(len(method_list)) + ") 行")
    else:
        logging.info("不是待提取文件")

    s.close_file()
    ###########################

    ####开始解析提取到的方法头 ####
    c = comfig_complier()

    # 定义两个列表 一个用来装外部可访问的方法 另一个用来装外部不能访问到的方法
    public_list = []
    unpublic_list = []
    info_list = []

    c.complier_start()

    for i in method_list:
        if type(i) != dict:
            if c.complier_method(i):
                public_list.append(i)
                logger.info("public -> "+i)
            else:
                unpublic_list.append(i)
                logger.info("unpublic -> "+i)
        else:
            try:
                info_list.append(i["package"].replace(";", "").strip())
                info_list.append(i["class"].replace("{", "").strip())
            except KeyError as e:
                logging.info(str(type(e))+"......"+str(e.args))

    c.complier_close()
    ###########################

    # 文件类信息 | 外部可访问API列表 | 内部可访问API列表 | 是否为可提取的类文件（非接口文件之类）
    return [info_list,public_list,unpublic_list,isClass]