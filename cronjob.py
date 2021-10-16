import os
import sys
sys.path.append(os.environ['SCTYS_PROJECT'] + '/global_parameters')
from global_parameters import Path
from crontab import CronTab, CronSlices


class Cronjob(CronTab):

    PYTHON_PATH = Path.ANACONDA_PATH + '/envs/{}/bin/python'  # project_name
    SCRIPT_FILE = '{}.py'  # script_name
    CRON_LOG_FILE = 'cron_{}.log'  # script_name

    def __init__(self, project, logger):
        super().__init__(user=Path.USER)
        self.project = project
        self.logger = logger
        self.python_path = self.PYTHON_PATH.format(project)

    def get_command_from_script_name(self, script_name, *args):
        full_script_path = os.path.join(Path.PROJECT_FOLDER, self.project, self.SCRIPT_FILE.format(script_name))
        cron_log_path = os.path.join(Path.LOG_FOLDER.format(self.project), self.CRON_LOG_FILE.format(script_name))
        command = ' '.join([self.python_path, full_script_path] + list(args))
        command += ' > ' + cron_log_path + ' 2>&1'
        return command

    def get_cronjob_if_exist(self, script_name, *args):
        command = self.get_command_from_script_name(script_name, *args)
        jobs = self.find_command(command)
        return next(jobs, None)

    def set_cronjob(self, script_name, *args, time_code):
        assert CronSlices.is_valid(time_code)
        cron_job = self.get_cronjob_if_exist(script_name, *args)
        if cron_job is None:
            command = self.get_command_from_script_name(script_name, *args)
            self.logger.debug('Command on crontab: {}'.format(command))
            cron_job = self.new(command=command)
        cron_job.setall(time_code)
        assert cron_job.is_valid()
        self.write()
        self.logger.info('Cron job for project {} script {} set with time setting {} and parameters {}'.format(
            self.project, script_name, time_code, args))

    def remove_cronjob(self, script_name, *args):
        cron_job = self.get_cronjob_if_exist(script_name, *args)
        if cron_job is None:
            self.logger.warning('Cron job for project {} script {} and parameters {} not found'.format(
                self.project, script_name, args))
        else:
            self.remove(cron_job)
            self.write()
            self.logger.info('Cron job for project {} script {} and parameters {} removed'.format(
                self.project, script_name, args))
