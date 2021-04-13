import logging
from dotenv import get_key
import pathlib


class AppLogs:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppLogs, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig \
            (level=logging.DEBUG,
             filename='/logs/app_tmp.log',
             filemode='w',
             format=log_format,
             datefmt='%d-%b-%y %H:%M:%S')
        self.logger = logging.getLogger()
        c_format = \
            logging.Formatter(fmt=log_format, datefmt='%d-%m-%y %H:%M:%S')
        # log - debug level and higher
        debug_log = logging.FileHandler('./logs/main.log')
        # log errors
        error_log = logging.FileHandler('./logs/errors.log')
        # if get_key('my_env.env', 'APP_PRODUCTION') == 'True':
        #     debug_log.setLevel(logging.ERROR)
        #     error_log.setLevel(logging.CRITICAL)
        # else:
        debug_log.setLevel(logging.DEBUG)
        error_log.setLevel(logging.ERROR)
        debug_log.setFormatter(c_format)
        error_log.setFormatter(c_format)
        self.logger.addHandler(error_log)
        self.logger.addHandler(debug_log)

    def get_log(self):
        return self.logger

