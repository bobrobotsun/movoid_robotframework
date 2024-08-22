import sys


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


def tracing(*args, **kwargs):
    print(args, kwargs)


sys.settrace(tracing)

print(globals())
print(locals())
temp1()
