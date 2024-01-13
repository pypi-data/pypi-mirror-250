import datetime
import os
import json

import inspect

from .__cls_aide_base__ import __cls_base__


class _cls_frame_func:
    @staticmethod
    def get_current_function_name():
        frame = inspect.currentframe()
        func_name = frame.f_back.f_code.co_name
        return func_name

    @staticmethod
    def is_directly_called(func):
        current_frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(current_frame)
        for frame in outer_frames:
            if frame[3] != func.__name__:
                return False
        return True


class _cls_rst_files(__cls_base__):
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

            log = self.cjson(log)

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


class _cls_aide_rst_base(__cls_base__):
    # noinspection PyMissingConstructor
    def __init__(self, module: str, log_level: int = -1):
        self.__dict_rst = {"state": False,
                           "msg": None,
                           "data": None,
                           "dur": None,
                           "process": "INIT",
                           "module": module}

        self.__terse_keys = ["state", "msg", "data"]

        self.__last_process = None

        self.state_True = True
        self.state_False = False
        self.state_Info = "Info"

        self.__last_process = None
        self.__last_process = None

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
            elif text.find(f"{self.file.conf_LOG_LEVEL}=2") >= 0:
                self.log_level = 2
            else:
                self.log_level = 3
        else:
            self.log_level = log_level

        if text.find(f"{self.file.conf_DEBUG}=1") >= 0:
            self.__debug = True
        else:
            self.__debug = False

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
            if new_state in [self.state_False]:
                self.add_log()
            else:
                pass
        elif self.log_level == 2:
            if new_state in [self.state_False, self.state_Info]:
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
        self.__last_process = self.process
        self.__dict_rst["process"] = new_process_name

    def set_process_back(self):
        self.__dict_rst["process"] = self.__last_process

    @property
    def all(self):
        return self.__dict_rst

    @property
    def terse(self):
        return {key: self.__dict_rst[key] for key in self.__terse_keys}

    @property
    def json(self, show_all: bool = False):
        if show_all is True:
            return self.cjson(self.all)
        else:
            return self.cjson(self.terse)

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
            if state == self.state_True:
                if self.__last_process is not None:
                    self.set_process_back()
                else:
                    pass
            else:
                self.set_process(f"{self.__last_process}.{self.process}")

        # fang zai zui hou ,chu fa ri zhi
        self.set_state(state)

    def print(self):
        print(self.all)

    def add_log(self):
        self.file.add_log(self.all)
        if self.__debug:
            self.print()
        else:
            pass
