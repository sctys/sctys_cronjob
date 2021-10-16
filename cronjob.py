import os
from crontab import CronTab, CronSlices


class Cronjob(CronTab):

    USER = os.environ['USER']
    PROJECT_PATH = os.environ['SCTYS_PROJECT']
    ANACONDA_PATH = os.environ['CONDA_PREFIX'].split('/env')[0]
    PYTHON_PATH = ANACONDA_PATH + '/envs/{}/bin/python'  # project_name
    SCRIPT_FILE = '{}.py'  # script_name

    def __init__(self, project, logger):
        super().__init__(user=self.USER)
        self.project = project
        self.logger = logger
        self.python_path = self.PYTHON_PATH.format(project)

    def get_command_from_script_name(self, script_name, *args):
        full_script_path = os.path.join(self.PROJECT_PATH, self.project, self.SCRIPT_FILE.format(script_name))
        command = ' '.join([self.python_path, full_script_path] + list(args))
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
