# encoding=utf-8
# coding=utf-8

from loguru import logger
from django.conf import settings


logger.add(settings.LOG_ROOT+'/log_debug.log', filter=lambda record: record["extra"]["name"] == "log_debug", rotation="10 MB", retention='10 days', level="ERROR", backtrace=True, diagnose=True)

logger.add(settings.LOG_ROOT+'/log_data.log', filter=lambda record: record["extra"]["name"] == "log_data", rotation="10 MB", retention='10 days', level="ERROR", backtrace=True, diagnose=True)

log_debug = logger.bind(name="log_debug")
log_data = logger.bind(name="log_data")


# 在其他文件中的用法

'''
from loguru_log import log_debug, log_data

log_debug.warning("This is a new log")

log_data.debug("this is a debug log")
'''

'''
from log import loguru_log

loguru_log.log_debug.warning("当前django运行版本:" + __version__)
'''

'''
logger.add('test_log.log', filter=lambda record: record["extra"]["name"] == "service_log", rotation="500 MB", retention='10 days', level="DEBUG", backtrace=True, diagnose=True)

logger_a = logger.bind(name="service_log")

logger_a.info("Message A")
'''




# 一般用法，在函数上面写装饰器@logger.catch

# @logger.catch
# @log_debug.catch
# 可以将该装饰器放在函数上方等，如果该语句段出现异常，会直接在cmd中打印出异常的调试信息，但是不会直接打印在文件中
# Eg:
# @logger.catch
# def my_function(x, y, z):
#     # An error? It's caught anyway!
#     return 1 / (x + y + z)

# my_function(0, 0, 0)


# logger.debug('this is a debug message')
# logger.info('this is another debug message')
# logger.warning('this is another debug message')
# logger.error('this is another debug message')
# logger.success('this is success message!')
# logger.critical('this is critical message!')


# def add(
#         self,
#         sink,
#         *,
#         level=_defaults.LOGURU_LEVEL,
#         format=_defaults.LOGURU_FORMAT,
#         filter=_defaults.LOGURU_FILTER,
#         colorize=_defaults.LOGURU_COLORIZE,
#         serialize=_defaults.LOGURU_SERIALIZE,
#         backtrace=_defaults.LOGURU_BACKTRACE,
#         diagnose=_defaults.LOGURU_DIAGNOSE,
#         enqueue=_defaults.LOGURU_ENQUEUE,
#         catch=_defaults.LOGURU_CATCH,
#         **kwargs
#     )

# logger.add('runtime.log', format="{time} {level} {message}", filter="my_module", level="INFO")
# logger.add('runtime_{time}.log', rotation="500 MB")

# logger.add('runtime_{time}.log', rotation='00:00')
# 每天 0 点新创建一个 log 文件输出

# logger.add('runtime_{time}.log', rotation='1 week')
# 每周 新创建一个 log 文件输出


# logger.add('runtime.log', retention='10 days')
# 日志文件最长保留10天

# logger.add('runtime.log', compression='zip')
# 日志压缩格式是 zip

# logger.info('If you are using Python {}, prefer {feature} of course!', 3.6, feature='f-strings')
# 有个博客说是《友好的格式化》，但是我感觉并不好用


# 如何记录到两个文件中

# 1. 根据 filter 区分 logger ，再用 logger.bind() 做 logger 的区分

# logger.add("../static/logs/a.log", filter=lambda record: record["extra"]["name"] == "service_log")
# logger.add("../static/logs/b.log", filter=lambda record: record["extra"]["name"] == "app_log")

# # 这个bind()函数就是在extra里额外增加键值
# logger_a = logger.bind(name="service_log")
# logger_b = logger.bind(name="app_log")

# logger_a.info("Message A")
# logger_b.info("Message B")

# 2. 根据日志等级记录到不同文件

# logger.add(path_log_info, level="INFO",filter=lambda x: 'INFO' in str(x['level']).upper())
# logger.add(path_log_error, level="INFO",filter=lambda x: 'ERROR' in str(x['level']).upper())

# 删除向日志文件中记录log
# trace = logger.add('runtime.log')
# logger.remove(trace)


