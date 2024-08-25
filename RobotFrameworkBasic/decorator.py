#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : decorator
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/12 18:12
# Description   : 这里记录了robotframework的一些将python函数生成一个日志组的函数。如果你当前运行的不是robot时，这个装饰器不会对函数进行改变
"""
import time

from movoid_function import type as function_type
from movoid_function import wraps, wraps_func, reset_function_default_value, analyse_args_value_from_function

from .version import VERSION

if VERSION:
    if VERSION == '6':
        import datetime
        import traceback
        from robot.running.model import Keyword as RunningKeyword
        from robot.result.model import Keyword as ResultKeyword
        from robot.running.modelcombiner import ModelCombiner  # noqa
        from robot.output.logger import LOGGER
        from robot.running.outputcapture import OutputCapturer


        def _robot_log_keyword(*return_is_fail):
            if len(return_is_fail) == 1 and callable(return_is_fail[0]):
                return _robot_log_keyword()(return_is_fail[0])
            else:
                return_is_fail = list(return_is_fail)

            def dec(func):
                if getattr(func, '_robot_log', None) is not None:
                    return func

                @wraps(func)
                def wrapper(*args, _return_when_error=None, _log_keyword_structure=True, **kwargs):
                    arg_dict = analyse_args_value_from_function(func, *args, _return_when_error=_return_when_error, _log_keyword_structure=_log_keyword_structure, **kwargs)
                    re_value = None
                    temp_error = None
                    if _log_keyword_structure:
                        data = RunningKeyword(func.__name__)
                        result = ResultKeyword(func.__name__,
                                               args=[f'{_i}:{type(_v).__name__}={_v}' for _i, _v in arg_dict.items() if _i != 'self'],
                                               doc=None if func.__doc__ is None else func.__doc__.replace('\n', '\n\n'))
                        result.starttime = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S.%f')[:-3]  # noqa
                        combine = ModelCombiner(data, result)
                        LOGGER.start_keyword(combine)
                        with OutputCapturer():
                            try:
                                re_value = func(*args, **kwargs)
                            except Exception as err:
                                result.status = 'FAIL'
                                print(traceback.format_exc())
                                if _return_when_error is not None:
                                    re_value = _return_when_error
                                else:
                                    temp_error = err
                            else:
                                print(f'{re_value}({type(re_value).__name__}):is return value')
                                if re_value in return_is_fail:
                                    result.status = 'FAIL'
                                else:
                                    result.status = 'PASS'
                        result.endtime = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S.%f')[:-3]  # noqa
                        LOGGER.end_keyword(combine)
                    else:
                        print(func.__name__, *[f'{_i}:{type(_v).__name__}={_v}' for _i, _v in arg_dict.items() if _i != 'self'])
                        try:
                            re_value = func(*args, **kwargs)
                        except Exception as err:
                            print(traceback.format_exc())
                            if _return_when_error is not None:
                                re_value = _return_when_error
                            else:
                                temp_error = err
                        else:
                            print(func.__name__, f'{re_value}({type(re_value).__name__}):is return value')
                    if temp_error is not None:
                        raise temp_error
                    else:
                        return re_value

                setattr(wrapper, '_robot_log', True)
                return wrapper

            return dec
    elif VERSION == '7':
        import datetime
        import traceback
        from robot.running.model import Keyword as RunningKeyword
        from robot.result.model import Keyword as ResultKeyword
        from robot.output.logger import LOGGER
        from robot.running.outputcapture import OutputCapturer


        def _robot_log_keyword(*return_is_fail):
            if len(return_is_fail) == 1 and callable(return_is_fail[0]):
                return _robot_log_keyword()(return_is_fail[0])
            else:
                return_is_fail = list(return_is_fail)

            def dec(func):
                if getattr(func, '_robot_log', None) is not None:
                    return func

                @wraps(func)
                def wrapper(*args, _return_when_error=None, _log_keyword_structure=True, **kwargs):
                    arg_dict = analyse_args_value_from_function(func, *args, _return_when_error=_return_when_error, _log_keyword_structure=_log_keyword_structure, **kwargs)
                    re_value = None
                    temp_error = None
                    if _log_keyword_structure:
                        data = RunningKeyword(func.__name__)
                        result = ResultKeyword(func.__name__,
                                               args=[f'{_i}:{type(_v).__name__}={_v}' for _i, _v in arg_dict.items() if _i != 'self'],
                                               doc=None if func.__doc__ is None else func.__doc__.replace('\n', '\n\n'))
                        result.start_time = datetime.datetime.now()
                        LOGGER.start_keyword(data, result)
                        with OutputCapturer():
                            try:
                                re_value = func(*args, **kwargs)
                                print(f'{re_value}({type(re_value).__name__}):is return value')
                            except Exception as err:
                                result.status = 'FAIL'
                                print(traceback.format_exc())
                                if _return_when_error is not None:
                                    re_value = _return_when_error
                                else:
                                    temp_error = err
                            else:
                                if re_value in return_is_fail:
                                    result.status = 'FAIL'
                                else:
                                    result.status = 'PASS'
                        result.end_time = datetime.datetime.now()
                        LOGGER.end_keyword(data, result)
                    else:
                        print(func.__name__, *[f'{_i}:{type(_v).__name__}={_v}' for _i, _v in arg_dict.items() if _i != 'self'])
                        try:
                            re_value = func(*args, **kwargs)
                        except Exception as err:
                            print(traceback.format_exc())
                            if _return_when_error is not None:
                                re_value = _return_when_error
                            else:
                                temp_error = err
                        else:
                            print(func.__name__, f'{re_value}({type(re_value).__name__}):is return value')
                    if temp_error is not None:
                        raise temp_error
                    else:
                        return re_value

                setattr(wrapper, '_robot_log', True)
                return wrapper

            return dec
    else:
        raise ImportError('robotframework should be 6 or 7. please pip install robotframework again')


else:
    def _robot_log_keyword(*return_is_fail):
        if len(return_is_fail) == 1 and callable(return_is_fail[0]):
            return _robot_log_keyword()(return_is_fail[0])

        def dec(func):
            if getattr(func, '_robot_log', None) is not None:
                return func

            @wraps(func)
            def wrapper(*args, _return_when_error=None, _log_keyword_structure=True, **kwargs):
                arg_dict = analyse_args_value_from_function(func, *args, _return_when_error=_return_when_error, _log_keyword_structure=_log_keyword_structure, **kwargs)
                print(func.__name__, *[f'{_i}:{type(_v).__name__}={_v}' for _i, _v in arg_dict.items() if _i != 'self'])
                re_value = None
                temp_error = None
                try:
                    re_value = func(*args, **kwargs)
                except Exception as err:
                    if _return_when_error is not None:
                        re_value = _return_when_error
                    else:
                        temp_error = err
                if temp_error is not None:
                    raise temp_error
                else:
                    print(f'{func.__name__}: {re_value}({type(re_value).__name__}):is return value')
                    return re_value

            setattr(wrapper, '_robot_log', True)
            return wrapper

        return dec

robot_log_keyword = _robot_log_keyword


def robot_no_log_keyword(func):
    setattr(func, '_robot_log', False)
    return func


def do_until_check(do_function, check_function, timeout=30, init_check=True, init_check_function=None, init_sleep=0, wait_before_check=0, do_interval=1, check_interval=0.2, error=True):
    """
    通过操作某个函数，达成某个最终的目的。如果检查未通过，那么会循环进行操作
    这是一个装饰器，需要套在一个空函数上（仅函数名会被继承）
        当然了，你也可以套在一个有价值的函数上，但是这个函数的所有痕迹都会被抹除
    :param do_function:主动操作的函数，传入函数，不需要返回值
    :param check_function:检查函数，返回值必须是一个bool值，或者返回值会被强制转换为bool
    :param timeout:最大时常/超时。检查超过这个时常后，会认为操作失败.
    :param init_check:是否进行初始检查，如果为True，那么会在操作前进行检查，如果通过，那么会跳过操作，直接结束
    :param init_check_function:初始检查函数，返回值必须是一个bool值，或者返回值会被强制转换为bool，如果存在。那么初始检查会考虑使用这个。这个函数的参数必须和check_function完全一致，否则会报错
    :param init_sleep:初始的等待时间，在初始检查前进行的等待，不计入整体timeout时间，一般配合初始检查init_check=True使用
    :param wait_before_check:在常规检查前的等待时间，一般是和上一次的操作存在一定的等待时间，保证上次的操作可以真实地
    :param do_interval:两次操作之间地最小间隔。一般是检查结束后，到操作之前的时间。主要是为了保证不要进行太多次的循环
    :param check_interval:连续两次检查之间的时间间隔，默认值为1，如果想要进行更细致的循环检查，可以将这个数值设置得更小
    :param error:当检查失败后，是否raise一个error。默认为True，会raise。
    :return: 返回是否判定成功，但是当error=True时，失败了会raise AssertionError，那也就不会有返回值了
    """
    _timeout = 30 if timeout is None else float(timeout)  # type:float
    _init_check = True if init_check is None else bool(init_check)  # type:bool
    init_check_function = check_function if init_check_function is None else init_check_function
    _init_sleep = 0 if init_sleep is None else float(init_sleep)  # type:float
    _wait_before_check = 1 if wait_before_check is None else float(wait_before_check)  # type:float
    _do_interval = 1 if do_interval is None else float(do_interval)  # type:float
    _check_interval = 0.2 if check_interval is None else float(check_interval)  # type:float
    _error = True if error is None else bool(error)  # type:bool

    def dec(func):
        @robot_log_keyword
        @wraps_func(func, do_function, check_function)
        def running_part(do_kwargs,
                         check_kwargs,
                         timeout=_timeout,  # noqa
                         init_check=_init_check,  # noqa
                         init_sleep=_init_sleep,  # noqa
                         wait_before_check=_wait_before_check,  # noqa
                         do_interval=_do_interval,  # noqa
                         check_interval=_check_interval,  # noqa
                         error=_error):  # noqa
            do_kwargs['_return_when_error'] = False
            check_kwargs['_return_when_error'] = False
            do_text = f'do {do_function.__name__}{do_kwargs}'
            print(f'do action:{do_text}')
            check_text = f'check {check_function.__name__}{check_kwargs}'
            print(f'check action:{check_text}')
            if init_check:
                print_text = ''
                try:
                    check_bool = init_check_function(**check_kwargs)
                    if check_bool:
                        print_text = f'pass init {check_text}.do_until_check end.'
                        return True
                    else:
                        print_text = f'fail init {check_text}.'
                except Exception as err:
                    print_text = f'error init {check_text}:{err}'
                finally:
                    if not getattr(init_check_function, '_robot_log', False):
                        print(print_text)
            time.sleep(init_sleep)
            total_time = 0
            start_time_point = time.time()
            loop_time = 0
            while total_time < timeout:
                total_interval_time_point = time.time()
                loop_time += 1
                print_text = ''
                try:
                    do_function(**do_kwargs)
                    print_text = f'end do {time.time() - start_time_point:.3f} second {loop_time} time'
                except Exception as err:
                    print_text = f'error do {time.time() - start_time_point:.3f} second {loop_time} time :{err}'
                finally:
                    if not getattr(do_function, '_robot_log', False):
                        print(print_text)
                time.sleep(wait_before_check)
                check_time = 0
                check_time_point = time.time()
                check_loop_time = 0
                while check_time < do_interval:
                    check_interval_time_point = time.time()
                    check_loop_time += 1
                    try:
                        check_bool = check_function(**check_kwargs)
                        time_now = time.time()
                        if check_bool:
                            print_text = f'pass check {time_now - start_time_point:.3f}/{time_now - check_time_point:.3f} second {loop_time}-{check_loop_time} time.do until check end.'
                            return True
                        else:
                            print_text = f'fail check {time_now - start_time_point:.3f}/{time_now - check_time_point:.3f} second {loop_time}-{check_loop_time} time.'
                    except Exception as err:
                        time_now = time.time()
                        print_text = f'error check {time_now - start_time_point:.3f}/{time_now - check_time_point:.3f} second {loop_time}-{check_loop_time} time:{err}'
                    finally:
                        if not getattr(check_function, '_robot_log', False):
                            print(print_text)
                    check_interval_time = time.time() - check_interval_time_point
                    if check_interval_time < check_interval:
                        time.sleep(check_interval - check_interval_time)
                    check_time = time.time() - check_time_point
                total_interval_time = time.time() - total_interval_time_point
                if total_interval_time < do_interval:
                    time.sleep(do_interval - total_interval_time)
                total_time = time.time() - start_time_point
            else:
                total_time = time.time() - start_time_point
                print_text = f'{total_time:.3f} second {loop_time} time {do_text} {check_text} fail.'
                if error:
                    return AssertionError(print_text)
                else:
                    print(print_text)
                    return False

        @robot_log_keyword
        def raising_part(err):
            raise err

        @wraps(running_part)
        def wrapper(*args, **kwargs):
            re_value = running_part(*args, **kwargs)
            if isinstance(re_value, Exception):
                raising_part(re_value)
            else:
                return re_value

        return wrapper

    return dec


def wait_until_stable(check_function, timeout=30, init_check=True, init_check_function=None, init_sleep=0, stable_time=3, check_interval=0.2, error=True):
    """
    通过操作某个函数，达成某个最终的目的。如果检查未通过，那么会循环进行操作
    这是一个装饰器，需要套在一个空函数上（仅函数名会被继承）
        当然了，你也可以套在一个有价值的函数上，但是这个函数的所有痕迹都会被抹除
    :param check_function:检查函数，返回值必须是一个bool值，或者返回值会被强制转换为bool
    :param timeout:限时。只有在这个时长范围内一直通过，才算成功.
    :param init_check:是否进行初始检查，如果为True，那j么会在操作前进行检查，如果通过，那么会跳过操作，直接结束
    :param init_check_function:初始检查函数，返回值必须是一个bool值，或者返回值会被强制转换为bool，如果存在。那么初始检查会考虑使用这个。这个函数的参数必须和check_function完全一致，否则会报错
    :param init_sleep:初始的等待时间，在初始检查前进行的等待，不计入整体timeout时间，一般配合初始检查init_check=True使用
    :param stable_time:需要达到的稳定状态的持续时间，只有一直判定正确超过这个时间，才能算过
    :param check_interval:连续两次检查之间的时间间隔，默认值为0.2，如果想要进行更细致的循环检查，可以将这个数值设置得更小
    :param error:当检查失败后，是否raise一个error。默认为True，会raise。
    :return: 返回是否判定成功，但是当error=True时，失败了会raise AssertionError，那也就不会有返回值了
    """
    _timeout = 3 if timeout is None else float(timeout)  # type:float
    _init_check = True if init_check is None else bool(init_check)  # type:bool
    init_check_function = check_function if init_check_function is None else init_check_function
    _init_sleep = 0 if init_sleep is None else float(init_sleep)  # type:float
    _stable_time = 3 if stable_time is None else float(stable_time)  # type:float
    _check_interval = 0.2 if check_interval is None else float(check_interval)  # type:float
    _error = True if error is None else bool(error)  # type:bool

    def dec(func):
        @robot_log_keyword
        @wraps_func(func, check_function)
        def running_part(check_kwargs,
                         timeout=_timeout,  # noqa
                         init_check=_init_check,  # noqa
                         init_sleep=_init_sleep,  # noqa
                         stable_time=_stable_time,  # noqa
                         check_interval=_check_interval,  # noqa
                         error=_error):  # noqa
            check_kwargs['_return_when_error'] = False
            check_text = f'check {check_function.__name__}{check_kwargs}'
            print(f'check action:{check_text}')
            if init_check:
                print_text = ''
                try:
                    check_bool = init_check_function(**check_kwargs)
                    if check_bool:
                        print_text = f'init {check_text} pass.'
                    else:
                        print_text = f'init {check_text} fail.'
                except Exception as err:
                    print_text = f'init {check_text} error:{err}'
                finally:
                    if not getattr(check_function, '_robot_log', False):
                        print(print_text)
            time.sleep(init_sleep)
            total_time = 0
            start_time_point = time.time()
            loop_time = 0
            pass_time = 0
            while total_time < timeout:
                total_interval_time_point = time.time()
                loop_time += 1
                print_text = ''
                try:
                    check_bool = check_function(**check_kwargs)
                    if check_bool:
                        print_text = '{:.3f} second {} time {} pass.'.format(time.time() - start_time_point, loop_time, check_text)
                        if pass_time == 0:
                            pass_time = time.time()
                            now_stable_time = 0
                        else:
                            now_stable_time = time.time() - pass_time
                        print_text += ' it has been stable for {:.3f} seconds.'.format(now_stable_time)
                        if now_stable_time > stable_time:
                            return True
                    else:
                        print_text = '{:.3f} second {} time {} fail.'.format(time.time() - start_time_point, loop_time, check_text)
                        pass_time = 0
                        print(print_text)
                except Exception as err:
                    print_text = '{:.3f} second {} time {} error:{}'.format(time.time() - start_time_point, loop_time, check_text, err)
                    pass_time = 0
                finally:
                    if not getattr(check_function, '_robot_log', False):
                        print(print_text)
                total_interval_time = time.time() - total_interval_time_point
                if total_interval_time < check_interval:
                    time.sleep(check_interval - total_interval_time)
                total_time = time.time() - start_time_point
            else:
                total_time = time.time() - start_time_point
                print_text = '{:.3f} second {} time {} all fail/error.do_until_check fail.'.format(total_time, loop_time, check_text)
                if error:
                    return AssertionError(print_text)
                else:
                    print(print_text)
                    return False

        @robot_log_keyword
        def raising_part(err):
            raise err

        @wraps(running_part)
        def wrapper(*args, **kwargs):
            re_value = running_part(*args, **kwargs)
            if isinstance(re_value, Exception):
                raising_part(re_value)
            else:
                return re_value

        return wrapper

    return dec


def always_true_until_check(do_function, check_function, timeout=30, init_sleep=0, wait_before_check=0, check_interval=0.2, error=True):
    """
    通过操作某个函数，达成某个最终的目的。如果检查未通过，那么会循环进行操作
    这是一个装饰器，需要套在一个空函数上（仅函数名会被继承）
        当然了，你也可以套在一个有价值的函数上，但是这个函数的所有痕迹都会被抹除
    :param do_function:必须保证一直正确的函数
    :param check_function:检查函数，返回值必须是一个bool值，或者返回值会被强制转换为bool
    :param timeout:最大时常/超时。检查超过这个时常后，会认为操作失败.
    :param init_sleep:初始的等待时间，在初始检查前进行的等待，不计入整体timeout时间，一般配合初始检查init_check=True使用
    :param wait_before_check:在常规检查前的等待时间，一般是和上一次的操作存在一定的等待时间，保证上次的操作可以真实地
    :param check_interval:连续两次检查之间的时间间隔，默认值为1，如果想要进行更细致的循环检查，可以将这个数值设置得更小
    :param error:当检查失败后，是否raise一个error。默认为True，会raise。
    :return: 返回是否判定成功，但是当error=True时，失败了会raise AssertionError，那也就不会有返回值了
    """
    _timeout = 30 if timeout is None else float(timeout)  # type:float
    _init_sleep = 0 if init_sleep is None else float(init_sleep)  # type:float
    _wait_before_check = 1 if wait_before_check is None else float(wait_before_check)  # type:float
    _check_interval = 0.2 if check_interval is None else float(check_interval)  # type:float
    _error = True if error is None else bool(error)  # type:bool

    def dec(func):
        @robot_log_keyword
        @wraps_func(func, do_function, check_function)
        def running_part(do_kwargs,
                         check_kwargs,
                         timeout=_timeout,  # noqa
                         init_sleep=_init_sleep,  # noqa
                         wait_before_check=_wait_before_check,  # noqa
                         check_interval=_check_interval,  # noqa
                         error=_error):  # noqa
            do_kwargs['_return_when_error'] = False
            check_kwargs['_return_when_error'] = False
            do_text = f'always true {do_function.__name__}{do_kwargs}'
            print(f'always true action:{do_text}')
            check_text = f'check {check_function.__name__}{check_kwargs}'
            print(f'check action:{check_text}')
            time.sleep(init_sleep)
            total_time = 0
            start_time_point = time.time()
            loop_time = 0
            while total_time < timeout:
                total_interval_time_point = time.time()
                loop_time += 1
                print_text = ''
                try:
                    do_bool = do_function(**do_kwargs)
                except Exception as err:
                    print_text = f'error always true {time.time() - start_time_point:.3f} second {loop_time} time :{err}'
                    if error:
                        return AssertionError(print_text)
                    else:
                        return False
                else:
                    time_now = time.time()
                    if do_bool:
                        print_text = f'pass always true {time_now - start_time_point:.3f} second {loop_time} time'
                    else:
                        print_text = f'fail always true {time_now - start_time_point:.3f} second {loop_time} time'
                        if error:
                            return AssertionError(print_text)
                        else:
                            return False
                finally:
                    if not getattr(do_function, '_robot_log', False):
                        print(print_text)
                time.sleep(wait_before_check)
                try:
                    check_bool = check_function(**check_kwargs)
                    time_now = time.time()
                    if check_bool:
                        print_text = f'pass check {time_now - start_time_point:.3f} second {loop_time} time.do until check end.'
                        return True
                    else:
                        print_text = f'fail check {time_now - start_time_point:.3f} second {loop_time} time.'
                except Exception as err:
                    time_now = time.time()
                    print_text = f'error check {time_now - start_time_point:.3f} second {loop_time} time:{err}'
                finally:
                    if not getattr(check_function, '_robot_log', False):
                        print(print_text)
                total_interval_time = time.time() - total_interval_time_point
                if total_interval_time < check_interval:
                    time.sleep(check_interval - total_interval_time)
                total_time = time.time() - start_time_point
            else:
                total_time = time.time() - start_time_point
                print_text = f'{total_time:.3f} second {loop_time} time {do_text} {check_text} fail.'
                if error:
                    return AssertionError(print_text)
                else:
                    print(print_text)
                    return False

        @robot_log_keyword
        def raising_part(err):
            raise err

        @wraps(running_part)
        def wrapper(*args, **kwargs):
            re_value = running_part(*args, **kwargs)
            if isinstance(re_value, Exception):
                raising_part(re_value)
            else:
                return re_value

        return wrapper

    return dec


def do_when_error(error_function):
    def dec(func):
        @wraps_func(func, error_function)
        def wrapper(kwargs, error_kwargs):
            try:
                re_value = func(**kwargs)
            except Exception as err:
                error_function(**error_kwargs)
                raise err
            else:
                return re_value

        return wrapper

    return dec


class Bool(function_type.Bool):
    def __init__(self, limit='', convert=True, **kwargs):
        super().__init__(limit=limit, convert=convert, **kwargs)


class Int(function_type.Int):
    def __init__(self, limit='', convert=True, **kwargs):
        super().__init__(limit=limit, convert=convert, **kwargs)


class Float(function_type.Float):
    def __init__(self, limit='', convert=True, **kwargs):
        super().__init__(limit=limit, convert=convert, **kwargs)


class Number(function_type.Number):
    def __init__(self, limit='', convert=True, **kwargs):
        super().__init__(limit=limit, convert=convert, **kwargs)


class Str(function_type.Str):
    def __init__(self, char=None, length='', regex=None, convert=True, **kwargs):
        super().__init__(char=char, length=length, regex=regex, convert=convert, **kwargs)


class List(function_type.List):
    def __init__(self, length='', convert=True, **kwargs):
        super().__init__(length=length, convert=convert, **kwargs)


class Tuple(function_type.Tuple):
    def __init__(self, length='', convert=True, **kwargs):
        super().__init__(length=length, convert=convert, **kwargs)


class Set(function_type.Set):
    def __init__(self, length='', convert=True, **kwargs):
        super().__init__(length=length, convert=convert, **kwargs)


class Dict(function_type.Dict):
    def __init__(self, length='', convert=True, **kwargs):
        super().__init__(length=length, convert=convert, **kwargs)


function_type.default_type = {
    bool: Bool,
    str: Str,
    int: Int,
    float: Float,
    list: List,
    set: Set,
    tuple: Tuple,
    dict: Dict,
}


@reset_function_default_value(function_type.check_parameters_type)
def check_parameters_type(convert=True, check_arguments=True, check_return=True):  # noqa
    pass
