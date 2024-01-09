import time
import logging
import os


# 设置日志文件路径
log_dir = './file'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_file = os.path.join(log_dir, 'log_file.log')


# 配置 logging
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s: %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def wrapper(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        result = end_time - start_time
        print('func time is %.6fs' % result)
        # 输出运行时间到日志文件
        logging.info('func time is %.6fs' % result)  
        return res

    return inner
