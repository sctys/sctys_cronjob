import sys
import os
import inspect
sys.path.append(os.environ['SCTYS_PROJECT'] + '/sctys_global_parameters')
from global_parameters import Path
sys.path.append(Path.UTILITIES_PROJECT)
from utilities_functions import set_logger
from cronjob import Cronjob


def test_set_cronjob():
    logger_path = Path.LOG_FOLDER + '/log_sctys_utilities'
    logger_file_name = inspect.currentframe().f_code.co_name + '.log'
    logger_name = inspect.currentframe().f_code.co_name
    logger_level = 'DEBUG'
    logger = set_logger(logger_path, logger_file_name, logger_level, logger_name)
    cron = Cronjob(Path.UTILITIES, logger)
    cron.set_cronjob('utilities_functions_test', time_code='* * * * *')


def test_remove_cronjob():
    logger_path = Path.LOG_FOLDER + '/log_sctys_utilities'
    logger_file_name = inspect.currentframe().f_code.co_name + '.log'
    logger_name = inspect.currentframe().f_code.co_name
    logger_level = 'DEBUG'
    logger = set_logger(logger_path, logger_file_name, logger_level, logger_name)
    cron = Cronjob(Path.UTILITIES, logger)
    cron.remove_cronjob('utilities_functions_test')


if __name__ == '__main__':
    # test_set_cronjob()
    test_remove_cronjob()


