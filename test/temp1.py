import sys

from RobotFrameworkBasic import robot_log_keyword


def temp1():
    print(__name__)
    print(locals())
    pass


class TempClass:
    @staticmethod
    def temp_static():
        pass

    @classmethod
    def temp_class(cls):
        pass

    def temp_self(self):
        pass


class TempClass2:
    @robot_log_keyword
    def temp_function1(self, _show_return_info=False):
    # def temp_function1(self):
        return 123


def tracing(*args, **kwargs):
    print(args, kwargs)


temp2 = TempClass2()
temp2.temp_function1()
# sys.settrace(tracing)
#
# print(globals())
# print(locals())
# temp1()
