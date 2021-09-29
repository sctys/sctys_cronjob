import sys
import os
import inspect
sys.path.append(os.environ['SCTYS_PROJECT'] + '/sctys_utilities')
from utilities_functions import set_logger
from cronjob import Cronjob


def test_set_cronjob():
    cron = Cronjob('sctys_utilities')
    logger_path = os.environ['SCTYS_PROJECT'] + '/Log/log_sctys_utilities'
    logger_file_name = inspect.currentframe().f_code.co_name + '.log'
    logger_name = inspect.currentframe().f_code.co_name
    logger_level = 'DEBUG'
    logger = set_logger(logger_path, logger_file_name, logger_level, logger_name)
    cron.set_cronjob('utilities_functions_test', time_code='* * * * *', logger=logger)


def test_remove_cronjob():
    cron = Cronjob('sctys_utilities')
    logger_path = os.environ['SCTYS_PROJECT'] + '/Log/log_sctys_utilities'
    logger_file_name = inspect.currentframe().f_code.co_name + '.log'
    logger_name = inspect.currentframe().f_code.co_name
    logger_level = 'DEBUG'
    logger = set_logger(logger_path, logger_file_name, logger_level, logger_name)
    cron.remove_cronjob('utilities_functions_test', logger=logger)


if __name__ == '__main__':
    # test_set_cronjob()
    test_remove_cronjob()


