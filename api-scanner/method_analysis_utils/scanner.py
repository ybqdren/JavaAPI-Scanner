# -*- coding:utf-8 -*-

# @Author: ZhaoWen <withzhaowen@126.com>
# @Date: 2021/3/17
# @GiteePath: https://gitee.com/openeuler2020/team-1186152014
import re
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def get_scanner():
    '''
    获取一个扫描器
    :return: m_scanner 返回一个scanner类的实例对象
    '''
    m_scanner = method_scanner.get_instance()
    return m_scanner

############### 定制一个switch ######################
def switcher(is_serious,str,token_type_dict):
    '''
    自定义一个switcher 用于token type的比较 用来判断没有已经固定死的内容
    :param is_serious: 是否为必要token
    :param str: 待判定的元素
    :param token_type_dict: token type 类型
    :return: a boolean value name result 返回True|False
    '''
    result = False
    if is_serious:
        # 判断传入的字符串是否符合必要token的格式
        if token_type_dict["imp_token"].check_token(str.strip()):
            result = True
    else:
        if token_type_dict["access_token"].check_token(str):
                result = True
        if token_type_dict["key_token"].check_token(str):
                result = True

    return result
############### /定制一个switch ######################

# Token类型
    # access_token 访问标识符 default public protected private
    # key_token 非访问标识符 + 关键字 final abstract static synchronized
    # invalid_token 无用字符标识符
    # imp_token 必要token
    # next_token 判断下一行token
class token_type():
    type = None
    reg_exp = ""

    def __init__(self,type,reg_exp=None):
        self.type = type
        self.reg_exp = reg_exp

    def get_token_type(self):
        '''
        获取token的类型
        :return: None
        '''
        return self.type

    def check_token(self,str):
        '''
        根据正则来判断传入的字符串是否符合token此type的规范
        :param str:
        :return:
        '''
        if re.search(self.reg_exp, str):
            return True
        else:
            return False

# 方法扫描器
class method_scanner():

    # 文件读取流
    file_stream = ""

    # token 类型列表
    token_type_dict = []

    # 存放临时字符串的全局变量
    temp_str = ""

    # 存放返回方法列表
    method_list = []

    # 用来确定方法范围的变量
    left_single = 0
    right_single = 0

    def __init__(self):
        logger.info("==================Code Scanner Start==================")

    def set_token_type(self,token_type_dict):
        '''
        传入一个类型集合
        :param token_type_dict:
        :return: None
        '''
        self.token_type_dict = token_type_dict

    def read_file(self,path):
        '''
        以io流的方式读取源代码文件
        :param path: 传入的单个文件地址
        :return: None
        '''
        try:
            self.file_stream = open(path,"r",encoding="utf-8")
        except FileNotFoundError as e:
            logging.info(str(type(e))+"......"+str(e.args))

    def close_file(self):
        '''
        关闭已经打开了的文件
        :return: None
        '''
        self.file_stream.close()
        logger.info("==================Code Scanner End==================")

    def clean_other(self,c):
        '''
        预先对代码中的无用元素进行清洗
        :return: a boolean value named result 用来检验是否为无用字符 True|False
        '''
        result = False

        # 是否为空行或注释
        if c == "" or re.match("^[/*\s]+(.*)", c):
            result = True
        # 是否为包信息或者导包信息
        elif c.startswith("import"):
            result = True
        # 是否为方法上方的注解
        elif c.startswith("@"):
            result = True

        return result

    def find_method(self):
        '''
        查找源码中的方法
        :return: a list named method_list 存储符合条件方法头的列表
        '''

        # 预先定义一个类信息字典
        minfo_dict = {"package":"","class":""}

        # 循环读取一个文件中的所有行
        while True:
            # 以行读取文件
            str_line = self.file_stream.readline()

            # 检测当前文件是否为空 或 是否已经遍历到文件末尾
            if str_line == "":
                break

            str_line = str_line.strip()

            # 根据传入字符串特征获取token信息
            token_type = self.get_token(str_line)

            # 是否为方法头
            if token_type.get_token_type() == "imp_token":
                method_result = ""

                # 意味着{ 出现一次 而此次也是方法出现的那次
                self.left_single += 1

                if self.temp_str.strip() != "":
                    self.temp_str += str_line.strip()
                    method_result = self.temp_str
                else:
                    method_result = str_line

                self.temp_str = ""
                self.method_list.append(method_result.replace("{","").strip())

            # 是否为多行方法头
            # 如
            #     public static <T> T parseObject(byte[] input, //
            #                                     int off, //
            #                                     int len, //
            #                                     CharsetDecoder charsetDecoder, //
            #                                     Type clazz, //
            #                                     Feature... features) {
            elif token_type.get_token_type() == "next_token":
                self.temp_str += str_line.strip().replace("//","")

            # 是否为包信息
            elif token_type.get_token_type() == "package_token":
                minfo_dict["package"] = str_line.replace("package", "").strip()

            # 是否为接口 接口不需要提取方法 直接跳出
            elif token_type.get_token_type() == "interface_token":
                self.method_list.append(False)
                return self.method_list

            # 是否为类 顺便存储一下类信息
            elif token_type.get_token_type() == "class_token":
                temp_list = str_line.split(" ")

                # 解决class中可能会有泛型<T>问题 比如'TypeReference<T>'
                try:
                    class_name = temp_list[temp_list.index("class") + 1]
                    minfo_dict["class"] = class_name[:class_name.index("<")]
                except ValueError as e:
                    minfo_dict["class"] = class_name

            # 判断是否为{}中的代码
            elif token_type.get_token_type() in ["left_single_token","right_single_token","all_single_token"]:
                if token_type.get_token_type() == "all_single_token":
                    self.left_single += 1
                    self.right_single += 1
                elif token_type.get_token_type() == "left_single_token":
                    self.left_single += 1
                elif token_type.get_token_type() == "right_single_token":
                    self.right_single += 1

                # 当{ 和 }个数相等时 意为着当前进入的方法结束
                if  self.left_single == self.right_single:
                    self.left_single = 0
                    self.right_single = 0

        # 将提取到的方法信息追加进结果集合中
        self.method_list.append(minfo_dict)
        # 设置为True 表示为类信息
        self.method_list.append(True)

        return self.method_list

    def get_token(self,str_line):
        '''
        根据其token类型判断token_type
        :param str_line: 待匹配的字符串
        :return: token_type
        '''

        # 判断是否为注释、空行或者导包之类的无用信息 这个条件一定要放在最前面，可以有效避免因注释中出现关键词而误判
        if self.clean_other(str_line):
            return token_type(type="invalid_token")

        # 判断是否为包信息
        if self.token_type_dict["package_token"].check_token(str_line):
            return token_type(type="package_token")

        # 判断是否为接口或者注解
        if self.token_type_dict["interface_token"].check_token(str_line):
            return token_type(type="interface_token")

        # 判断是否为类
        if self.token_type_dict["class_token"].check_token(str_line):
            return token_type(type="class_token")

        # 'private static void config(Properties properties) {'
        l_line = str_line.replace("("," (").split(" ")

        imp_token_str = ""
        for i in l_line:
            # 对非必要维度的token进行计算 access_token && key_token
            if switcher(False,i,self.token_type_dict):
                continue

            imp_token_str += i+" "

        # 判断是否存在 //
        if self.left_single == 0:
            if imp_token_str.strip().endswith("//"):
                return token_type("next_token")

        # 如果方法头中有 // 那么需要通过这个分支来判断
        if self.temp_str != "":
            if self.token_type_dict["next_method_token"].check_token(imp_token_str):
                self.left_single += 1
                return token_type(type="imp_token")

        # {} 都存在
        if self.token_type_dict["all_single_token"].check_token(imp_token_str):
            return token_type(type = "all_single_token")

        # {存在
        elif self.token_type_dict["left_single_token"].check_token(imp_token_str):
            if self.left_single == 0:
                if switcher(True, imp_token_str, self.token_type_dict):
                    return token_type(type="imp_token")
            return  token_type("left_single_token")

        # } 存在
        elif self.token_type_dict["right_single_token"].check_token(imp_token_str):
            return token_type("right_single_token")

        return token_type(type="invalid_token")

    @classmethod
    def get_instance(cls):
        '''
        获取一个scanner类实例对象
        :type @classmethod
        :return:
        '''
        return method_scanner()



