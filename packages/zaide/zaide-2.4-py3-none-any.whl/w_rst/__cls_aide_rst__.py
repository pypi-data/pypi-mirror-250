import datetime
import time
import os
import json
import socket

import inspect


def get_current_function_name():
    frame = inspect.currentframe()
    func_name = frame.f_back.f_code.co_name
    return func_name


class jsonDate(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class _cls_base:
    def __init__(self):
        pass

    @property
    def slash(self):
        if os.name == 'nt':
            return '\\'
        else:
            return '/'

    class cls_dict:
        def __init__(self):
            self.__my_dict = {}

        def add(self, new_key, new_value=None):
            self.__my_dict[new_key] = new_value

        def get(self, my_key):
            return self.__my_dict[my_key]

    @staticmethod
    def unix_timestamp_to_time_str(target_unix_timestamp: int):
        time0 = time.localtime(target_unix_timestamp)
        time0 = time.strftime("%Y-%m-%d %H:%M:%S", time0)

        return time0

    @staticmethod
    def hostname():
        return socket.gethostname()

    @property
    def ip(self):
        return socket.gethostbyname(self.hostname())

    @staticmethod
    def CrLf():
        return "\r\n"

    @staticmethod
    def cjson(data):
        return json.dumps(data, ensure_ascii=False, cls=jsonDate)

    @staticmethod
    def none_to_blank(value):
        if value is None:
            return ''
        else:
            return value

    @staticmethod
    def str_to_json(data):
        return json.loads(data)

    @staticmethod
    def dict_to_str(my_dict: dict,
                    split_key: str = "",
                    next_row_key: str = "\r\n",
                    pass_none: bool = False,
                    list_pass_name: list = None):
        s = None
        for key in my_dict:
            if list_pass_name is None or key not in list_pass_name:
                if s is None:
                    s = key + split_key + str(my_dict[key])
                else:
                    value = my_dict[key]

                    if value is None and pass_none is True:
                        pass
                    else:
                        if value is None:
                            value = ''
                        else:
                            value = str(value)

                        s = s + next_row_key + key + split_key + value
            else:
                pass
        return s

    @staticmethod
    def list_to_str(my_list, split_key: str = "", next_row_key: str = "\r\n", show_index_id: bool = True):
        s = None
        for i in my_list:

            if i is None:
                i = ''
            else:
                i = str(i)

            if s is None:
                if show_index_id is True:
                    s = str(i.index) + split_key + i
                else:
                    s = i

            else:
                if show_index_id is True:
                    s = s + str(i.index) + split_key + i
                else:
                    s = s + next_row_key + i
        return s

    @staticmethod
    def append(s, key, new_s):
        # print(s,new_s)
        # str_append = ""
        if s is None or s == "":
            if new_s is None or new_s == "":
                str_append = ""
            else:
                str_append = new_s
        else:
            if new_s is None or new_s == "":
                str_append = s
            else:
                str_append = str(s) + key + str(new_s)
        # print(str_append)
        if str_append is None:
            str_append = ""
        else:
            pass

        return str_append

    @staticmethod
    def is_ip(value):
        if not isinstance(value, str):
            return False
        else:
            pass

        if len(value) < 7 or len(value) > 15:
            # print(1)
            return False
        else:
            pass

        list_value = value.split(".")

        if len(list_value) != 4:
            # print(2)
            return False
        else:
            pass

        for s in list_value:
            if not s.isalnum():
                # print(3)
                return False
            else:
                if int(s) > 255 or int(s) < 0:
                    # print(4)
                    return False
                else:
                    pass

        if list_value[3] == '0':
            return False
        else:
            pass

        return True

    def find_ip(self, value: str, split_key: str = " "):
        ip = None
        if value is None:
            return None
        else:
            arr = value.split(split_key)

            for s in arr:
                if self.is_ip(s):
                    ip = s
                    return ip
                else:
                    pass

            return ip

    @staticmethod
    def first(my_value: str, my_split_key: str = ","):
        arr = str(my_value).split(my_split_key)
        return arr[0]

    def rcut(self, str0: str, start_key, start_count, start_correction, end_key, end_count, end_correction):
        # print(start_key,start_correction)
        start_index = self.rfindx(str0, start_key, start_count) + start_correction

        end_index = self.rfindx(str0, end_key, end_count) + end_correction

        # print(start_index, end_index)

        str_cut = str0[start_index:end_index]

        return str_cut

    @staticmethod
    def rfindx(str_source: str, str_key: str, count: int = 1):
        if str_key is None:
            return len(str_source)
        else:
            count0 = 1
            index = str_source.rfind(str_key)
            if index != -1:

                while count0 < count:
                    index = str_source[:index].rfind(str_key)
                    count0 = count0 + 1
                    # print(index, count0, count)
                    if index == -1:
                        return index
                    else:
                        pass

                return index
            else:
                return index

    @staticmethod
    def __cut_from_the_x_key_to_the_rest_first_key(str0: str,
                                                   start_key: str, start_key_order: int,
                                                   end_key: str,
                                                   include_start_key: bool = False, include_end_key: bool = False):

        if start_key == '':
            start_index = 0
        else:
            if start_key_order == 1:
                start_index = str0.find(start_key)
            elif start_key_order == -1:
                start_index = str0.rfind(start_key)
            else:
                start_index = str0.rfind(start_key)

        if include_start_key is False:
            start_index = start_index + len(start_key)
        else:
            pass

        str0 = str0[start_index:]

        end_index = str0.find(end_key)

        if include_end_key is False:
            pass
        else:
            end_index = end_index + len(end_key)

        str0 = str0[:end_index]

        return str0

    def cut_from_the_first_key_to_the_rest_first_key(self, str0: str,
                                                     start_key: str, end_key: str,
                                                     include_start_key: bool = False, include_end_key: bool = False):
        return self.__cut_from_the_x_key_to_the_rest_first_key(str0=str0,
                                                               start_key=start_key,
                                                               start_key_order=1,
                                                               end_key=end_key,
                                                               include_start_key=include_start_key,
                                                               include_end_key=include_end_key)

    def cut_from_the_last_key_to_the_rest_first_key(self, str0: str,
                                                    start_key: str, end_key: str,
                                                    include_start_key: bool = False, include_end_key: bool = False):
        return self.__cut_from_the_x_key_to_the_rest_first_key(str0=str0,
                                                               start_key=start_key,
                                                               start_key_order=-1,
                                                               end_key=end_key,
                                                               include_start_key=include_start_key,
                                                               include_end_key=include_end_key)

    def cut(self, str0: str, start_key, start_count, start_correction, end_key, end_count, end_correction):

        start_index = self.findx(str0, start_key, start_count) + start_correction

        end_index = self.findx(str0, end_key, end_count) + end_correction

        # print('start_key=', start_key)
        # print('start_index=', start_index,'end_index=', end_index)

        # print("se:", start_index, end_index)

        str_cut = str0[start_index:end_index]

        return str_cut

    def cut2(self, str0: str, start_key, start_count, start_correction, end_key, end_count, end_correction):

        start_index = self.findx(str0, start_key, start_count) + start_correction

        str1 = str0[start_index + len(start_key):]

        if end_count == 0:
            end_index = len(str1)
        elif end_count < 0:
            end_index = self.rfindx(str1, end_key, 0 - end_count) + end_correction
        else:
            end_index = self.findx(str1, end_key, end_count) + end_correction
        # print("se:", start_index, end_index)

        str_cut = str1[:end_index]

        # print('start_key=', start_key)
        # print('start_index=', start_index, 'end_index=', end_index)
        # print('str1=', str1)
        # print('str_cut=', str_cut)
        return str_cut

    @staticmethod
    def findx(str0: str, str1: str, count: int = 1):
        count0 = 1

        index = str0.find(str1)

        index_rst = index

        if index != -1:
            while count0 < count:
                # print(count0, "-", index_rst)

                index = str0[index_rst + len(str1):].find(str1)

                # print(count0, "--", index)

                if index == -1:
                    return index_rst
                else:
                    index_rst = index_rst + len(str1) + index

                    # print(count0, "---", index_rst)

                count0 = count0 + 1
            return index_rst
        else:
            return index_rst

    @property
    def no_such_key(self):
        return 'NoSuchKey'

    @staticmethod
    def get_dict_value(my_dict: dict, key: str, miss_key_default: str = "@#$"):
        if my_dict.__contains__(key):
            value = my_dict[key]
        else:
            if miss_key_default == "@#$":
                value = None
            else:
                value = miss_key_default
        return value


class _cls_rst_files(_cls_base):
    # noinspection PyMissingConstructor
    def __init__(self, rst_dir: str = None):
        self.rst_dir = rst_dir

        self.conf_DATE = "[INIT_DATE_UTC]"
        self.conf_LOG_LEVEL = "[LOG_LEVEL]"
        self.conf_DEBUG = "[DEBUG]"

        self.conf_file_path = None
        self.check_path(check_log_file=False, check_config_file=True)

    @property
    def log_file_path(self):
        return self.rst_dir + self.slash + "log" + self.slash + f"rst_{datetime.date.today()}.log"

    def check_path(self, check_config_file: bool = False, check_log_file: bool = True):
        now_path = os.getcwd()

        arr_now_path = now_path.split(self.slash)

        my_dir = None

        for i in arr_now_path:
            dir_name = i
            if dir_name != 'module':
                if my_dir is None:
                    my_dir = dir_name
                else:
                    my_dir = my_dir + self.slash + dir_name
            else:
                break

        self.rst_dir = my_dir + self.slash + "rst"

        self.conf_file_path = self.rst_dir + self.slash + "conf" + self.slash + "rst.conf"

        if not os.path.exists(self.rst_dir):
            os.mkdir(self.rst_dir)
            check_log_file = True
            check_config_file = True
        else:
            pass

        if check_config_file:

            path, file_name = os.path.split(self.conf_file_path)

            if not os.path.exists(path):
                os.mkdir(path)
            else:
                pass

            if not os.path.exists(self.conf_file_path):

                f = open(self.conf_file_path, 'a', encoding='utf-8')

                f.writelines(f"{self.conf_DATE}={datetime.datetime.utcnow()}")
                f.writelines("\n")
                f.writelines(f"{self.conf_LOG_LEVEL}=1")
                f.writelines("\n")
                f.writelines(f"{self.conf_DEBUG}=0")

                f.close()
            else:
                pass
        else:
            pass

        if check_log_file:
            path, file_name = os.path.split(self.log_file_path)

            if not os.path.exists(path):
                os.mkdir(path)
            else:
                pass

    def add_log(self, new_log):
        if self.log_file_path is None:
            self.check_path()
        else:
            pass

        try:
            f = open(self.log_file_path, 'a', encoding='utf-8')
            f.writelines("\n")

            log = {'gmt0': datetime.datetime.utcnow(), 'rst': new_log}

            log = json.dumps(log, ensure_ascii=False, cls=jsonDate)

            f.writelines(log)

            f.close()
        except Exception as e:
            # self.set_error(e.__str__())
            print("Log Write Error:" + e.__str__())

    @staticmethod
    def add_log_2(new_msg, log_path):
        f = open(log_path, 'a')
        f.writelines("\n")
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        f.writelines(new_msg)
        f.close()

    @staticmethod
    def find_log(new_msg, log_path):
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        return new_msg in open(log_path, 'rt').read()

    @staticmethod
    def replace_log(new_msg, log_path):
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        return new_msg in open(log_path, 'rt').read()

    @staticmethod
    def find_big_log(new_msg, log_path):
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        with open(log_path, 'rt') as handle:
            for ln in handle:
                if new_msg in ln:
                    return True
                else:
                    return False


class _cls_aide_rst_base(_cls_base):
    # noinspection PyMissingConstructor
    def __init__(self, module: str, log_level: int = -1):
        self.__dict_rst = {"state": False,
                           "msg": None,
                           "data": None,
                           "dur": None,
                           'process': "INIT",
                           'module': module}

        self.file = _cls_rst_files()

        # check eviroment and set log_level
        f = open(self.file.conf_file_path, 'r')

        text = f.read()

        f.close()

        if log_level not in [0, 1, 2, 3]:
            if text.find(f"{self.file.conf_LOG_LEVEL}=0") >= 0:
                self.log_level = 0
            elif text.find(f"{self.file.conf_LOG_LEVEL}=1") >= 0:
                self.log_level = 1
            elif text.find(f"{self.file.conf_LOG_LEVEL}=3") >= 0:
                self.log_level = 2
            else:
                self.log_level = 3
        else:
            self.log_level = log_level

        if text.find(f"{self.file.conf_DEBUG}=1") >= 0:
            self.debug = True
        else:
            self.debug = False

        self.start_time = None

    @staticmethod
    def now():
        return datetime.datetime.now()

    @property
    def dur(self,
            my_time_earlier: datetime.datetime = None,
            my_time_later: datetime.datetime = None):

        if my_time_later is None:
            my_time_later = datetime.datetime.now()
        else:
            pass

        if my_time_earlier is None:
            if isinstance(self.start_time, datetime.datetime):
                my_time_earlier = self.start_time
            else:
                return None
        else:
            pass

        diff_second = (my_time_later - my_time_earlier).seconds

        return diff_second

    @staticmethod
    def __get_dict_value(my_dict_rst, my_key):
        if my_dict_rst.__contains__(my_key):
            return my_dict_rst[my_key]
        else:
            return None

    @property
    def state(self):
        return self.__get_dict_value(self.__dict_rst, "state")

    def set_state(self, new_state: bool = False):
        self.__dict_rst["state"] = new_state

        if self.log_level == 0:
            pass
        elif self.log_level == 1:
            if new_state in [False]:
                self.add_log()
            else:
                pass
        elif self.log_level == 2:
            if new_state in [False, 2]:
                self.add_log()
            else:
                pass
        elif self.log_level == 3:
            self.add_log()

    @property
    def msg(self):
        return self.__get_dict_value(self.__dict_rst, "msg")

    def set_msg(self, new_msg: object = None):
        self.__dict_rst["msg"] = new_msg

    @property
    def data(self):
        return self.__get_dict_value(self.__dict_rst, "data")

    def set_data(self, new_data: object = None):
        self.__dict_rst["data"] = new_data

    @property
    def process(self):
        return self.__get_dict_value(self.__dict_rst, "process")

    def set_process(self, new_process_name: str = None):
        self.__dict_rst["process"] = new_process_name

    @property
    def all(self):
        return self.__dict_rst

    def set(self, new_state: object, new_msg: object = None, new_data: object = None, new_process: str = None):

        if isinstance(new_state, dict):
            state = new_state["state"]
            msg = new_state["msg"]
            data = new_state["data"]
        else:
            state = new_state
            msg = new_msg
            data = new_data

        self.set_msg(msg)
        self.set_data(data)
        if new_process is not None:
            self.set_process(new_process)
        else:
            pass

        # fang zai zui hou ,chu fa ri zhi
        self.set_state(state)

    def print(self):
        print(self.all)

    def add_log(self):
        self.file.add_log(self.all)
        if self.debug:
            self.print()
        else:
            pass
