import logging

import jenkins
from opsdroid.skill import Skill
from opsdroid.matchers import match_regex


_LOGGER = logging.getLogger(__name__)


def parse_params(parameters):
    return {key: value for key, value in [
        param.split('=') for param in parameters.split()]}


class JenkinsAPI(object):
    def __init__(self, jenkins):
        self._server = jenkins
        self.user = self._server.get_whoami()
        self.version = self._server.get_version()

    @property
    def server(self):
        return self._server.server

    @property
    def jobs(self):
        return self._server.get_jobs()

    @property
    def job_names(self):
        return [job['name'] for job in self.jobs]

    def run(self, job, parameters=None):
        if job in self.job_names:
            params = parse_params(parameters)
            self._server.build_job(job, params)
            return self._server.get_job_info(job)
        else:
            raise Exception("Unknown job: {}".format(job))


class JenkinsSkill(Skill):
    def __init__(self, opsdroid, config):
        super(JenkinsSkill, self).__init__(opsdroid, config)
        self.jenkins = JenkinsAPI(jenkins.Jenkins(
            config['url'],
            config['username'],
            config['password'],
        ))
        _LOGGER.info(self.me)

    @property
    def me(self):
        return 'At {} (v. {}), I am {}'.format(
            self.jenkins.server,
            self.jenkins.version,
            self.jenkins.user['fullName'],
        )

    @match_regex(r'list')
    async def list_jobs(self, message):
        job_list = "\n".join(self.jenkins.job_names)
        await message.respond(job_list)

    @match_regex(r'build ([^ ]*)(.*)')
    async def build_job(self, message):
        job_name = message.regex.group(1)
        parameters = message.regex.group(2).strip()
        response = "Building {}".format(job_name)
        if parameters != '':
            response += " with parameters {}".format(parameters)
        else:
            response += " without parameters"
        job_info = self.jenkins.run(job_name, parameters)
        response += " ({})".format(job_info['url'])
        await message.respond(response)
