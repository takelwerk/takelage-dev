#!/usr/bin/env python3

import argparse
from builtins import FileNotFoundError
from grp import getgrnam
import logging
from os import chown
from pathlib import Path
import subprocess
import yaml


class EntryPoint(object):

    def __init__(self):
        self._init_args_()
        self._init_vars_()
        self._init_logger_()

    def _init_args_(self):
        args = self._get_args_()
        self._debug = args.debug
        self._bit = args.bit
        self._docker = args.docker
        self._gid = args.gid
        self._git = args.git
        self._gopass = args.gopass
        self._gpg = args.gpg
        self._ssh = args.ssh
        self._username = args.username
        self._uid = args.uid
        self._homedir = Path(args.home)

    def _init_vars_(self):

        # hostdir: host home directory mapped do docker container
        self._hostdir = Path('/hostdir')

        # homedir: home directory in docker container (/home/my_user)
        self._mkdir_homedir_parent_(self._homedir)

        self._mapping_directories = {}

        # gpg agent and gpg ssh agent which are tunneled
        # via socat from host to docker container
        self._agent_forwards = {
            'gpg-agent': {
                'path': str(self._homedir) + '/.gnupg/S.gpg-agent',
                'port': 20000},
            'gpg-agent.ssh': {
                'path': str(self._homedir) + '/.gnupg/S.gpg-agent.ssh',
                'port': 20001}}

    def _init_logger_(self):
        # logger
        self._logger = self._logger_init_(self._debug)
        self._logger.debug('*************************')
        self._logger.debug('Starting configuration...')
        self._logger.debug('username: ' + self._username)
        self._logger.debug('userid: ' + str(self._uid))
        self._logger.debug('groupid: ' + str(self._gid))
        self._logger.debug('homedir: ' + str(self._homedir))
        self._logger.debug('bit: ' + str(self._bit))
        self._logger.debug('debug: ' + str(self._debug))
        self._logger.debug('git: ' + str(self._git))
        self._logger.debug('gopass: ' + str(self._gopass))
        self._logger.debug('gpg: ' + str(self._gpg))
        self._logger.debug('ssh: ' + str(self._ssh))

    def add_bit(self):
        if not self._bit:
            return

        # bit directories
        self._mkdir_homedir_child_('Library/Caches/Bit/logs')
        self._mkdir_homedir_child_('Library/Caches/Bit/config')

        # bit config
        bit_config_template = """
{"analytics_id":"40599udvk6jhxplr","analytics_reporting":false,"error_reporting":false}
"""
        bit_config_file = \
            self._homedir / 'Library/Caches/Bit/config/config.json'
        bit_config_file.write_text(bit_config_template)

        # ~/takelage.yml
        self._mapping_directories['.takelage.yml'] = self._hostdir

        self._logger.debug('bit config added')

    def add_docker(self):
        docker_config_template = """
{
  "credHelpers": {
    "gcr.io": "gcloud",
    "us.gcr.io": "gcloud",
    "eu.gcr.io": "gcloud",
    "asia.gcr.io": "gcloud",
    "staging-k8s.gcr.io": "gcloud",
    "marketplace.gcr.io": "gcloud"
  }
}
"""
        self._mkdir_homedir_child_('.docker')
        docker_config_file = self._homedir / '.docker/config.json'
        docker_config_file.write_text(docker_config_template)
        chown(str(docker_config_file), self._uid, self._gid)
        self._logger.debug('docker config added.')

    def add_gcloud(self):
        gcloud_system_path = Path('/srv/gcloud')
        if gcloud_system_path.exists():
            self._mkdir_homedir_child_('.config')
            gcloud_config_path = self._homedir / '.config/gcloud'
            gcloud_config_path.symlink_to(gcloud_system_path)
            self._logger.debug('gcloud config added')

    def add_git(self):
        if not self._git:
            return
        self._mapping_directories['.gitconfig'] = self._hostdir
        self._logger.debug('git config added')

    def add_gopass(self):
        if not self._gopass:
            return
        gopass_config_path = self._hostdir / '.config/gopass/config.yml'

        try:
            gopass_config = yaml.safe_load(
                gopass_config_path.read_text(encoding='utf-8'))
        except FileNotFoundError:
            self._logger.warning(
                'No gopass config file found: gopass is unavailable.')
            self._gopass = False
            return False

        # add config
        self._mkdir_homedir_child_('.config')
        self._mapping_directories['.config/gopass'] = self._hostdir

        # add path for the personal passwordstore
        if 'path' in gopass_config['root']:
            gopass_config_root_path = gopass_config['root']['path']
            root_path = Path(gopass_config_root_path.split(':', 1)[1])
            passwordstore_relpath = root_path.relative_to(self._homedir)
            self._mapping_directories[passwordstore_relpath] = \
                self._hostdir

        # add paths for mountet passwordstores
        for mount in gopass_config['mounts']:
            gopass_config_mount = gopass_config['mounts'][mount]
            if 'path' in gopass_config_mount:
                gopass_config_mount_path = gopass_config_mount['path']
                mount_path = Path(gopass_config_mount_path.split(':', 1)[1])
                passwordstore_relpath = mount_path.relative_to(self._homedir)
                self._mapping_directories[passwordstore_relpath] = \
                    self._hostdir
        self._logger.debug('gopass config added')
        return True

    def add_gpg(self):
        if not self._gpg:
            return

        # files should used from the host system
        gpg_links = [
            'pubring.kbx',
            'trustdb.gpg',
            'private-keys-v1.d',
            'openpgp-revocs.d',
            'crls.d']

        self._mkdir_homedir_child_('.gnupg')
        (self._homedir / '.gnupg').chmod(0o700)
        for item in gpg_links:
            self._mapping_directories[Path('.gnupg') / item] = \
                self._hostdir

        # files should ignored from the host system
        self._mapping_directories[Path('.gnupg/gpg-agent.conf')] = Path('/srv')
        self._mapping_directories[Path('.gnupg/gpg.conf')] = Path('/srv')
        self._mapping_directories[Path('.gnupg/dirmngr.conf')] = Path('/srv')
        self._logger.debug('gpg config added')

    def add_mapping(self):
        for item, path in self._mapping_directories.items():
            (self._homedir / item).symlink_to(path / item)

        # make tty read/writeable for user
        tty_device = subprocess.run(
            'tty',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.decode('utf-8').strip('\n')

        chown(tty_device, self._uid, -1)
        if self._docker:
            chown('/var/run/docker.sock', 0, getgrnam('docker').gr_gid)
        self._logger.debug('Directory mappings added')

    def add_ssh(self):
        if not self._ssh:
            return
        self._mapping_directories['.ssh'] = self._hostdir
        self._logger.debug('ssh config added')

    def add_user(self):
        self._logger.debug('Create user %s' % self._username)

        groups = 'sudo,tty'

        if self._docker:
            groups += ',docker'

        self._add_group_()

        useradd_command = [
            'useradd',
            '--create-home',
            '--home-dir', str(self._homedir),
            '--gid', str(self._gid),
            '--uid', str(self._uid),
            '--groups', groups,
            '--shell', '/bin/bash',
            '--non-unique',
            self._username]

        useradd_result = subprocess.run(
            useradd_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        if useradd_result.returncode:
            self._logger.error(useradd_result.stdout)
            self._logger.error(useradd_result.stderr)
            return False
        self._logger.debug('User added')

        # cp /root/.bashrc ~/.bashrc
        src = Path('/root/.bashrc')
        dest = self._homedir / '.bashrc'
        dest.write_text(src.read_text())

        # mkdir ~/.bashrc.d
        self._mkdir_homedir_child_('.bashrc.d')

        return True

    def forward_agents(self):
        self._logger.debug('Forwarding agents')
        for agent in self._agent_forwards:
            path = self._agent_forwards[agent]['path']
            port = self._agent_forwards[agent]['port']
            command = [
                '/usr/bin/socat',
                'UNIX-LISTEN:' + path +
                ',reuseaddr,fork,' +
                'user=' + self._username +
                ',gid=' + str(self._gid),
                'TCP:host.docker.internal:' +
                str(port)]

            self._logger.debug('Running command: ' + ' '.join(command))

            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

    def _add_group_(self):
        groupadd_command = ['groupadd',
                            '--gid', str(self._gid),
                            '--non-unique',
                            self._username]
        groupadd_result = subprocess.run(
            groupadd_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        if groupadd_result.returncode:
            self._logger.error(groupadd_result.stdout)
            self._logger.error(groupadd_result.stderr)
            return False

        return True

    def _get_args_(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Set debug flag.")
        parser.add_argument(
            "--gid",
            type=int,
            help="Group ID of the username used in the host system")
        parser.add_argument(
            "--home",
            type=str,
            help="Home directory used in the host system")
        parser.add_argument(
            "--no-bit",
            dest="bit",
            action="store_false",
            default=True,
            help="Do not add bit configuration")
        parser.add_argument(
            "--no-docker",
            dest="docker",
            action="store_false",
            default=True,
            help="Disable docker-socket passthrough")
        parser.add_argument(
            "--no-git",
            dest="git",
            action="store_false",
            default=True,
            help="Do not add git configuation")
        parser.add_argument(
            "--no-gopass",
            dest="gopass",
            action="store_false",
            default=True,
            help="Do not add gopass configuration")
        parser.add_argument(
            "--no-gpg",
            dest="gpg",
            action="store_false",
            default=True,
            help="Do not add gpg configuration")
        parser.add_argument(
            "--no-ssh",
            dest="ssh",
            action="store_false",
            default=True,
            help="Do not add ssh configuration")
        parser.add_argument(
            "--uid",
            type=int,
            help="User ID of the username used in the host system")
        parser.add_argument(
            "--username",
            type=str,
            help="Username used in the host system")
        return parser.parse_args()

    def _logger_init_(self, debug):
        logger = logging.getLogger(__file__)
        logger.setLevel(logging.INFO)
        if debug:
            logger.setLevel(logging.DEBUG)
        Path('/debug').mkdir(exist_ok=True)
        fh = logging.FileHandler('/debug/takelage.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def _mkdir_homedir_child_(self, directory):
        dir = self._homedir / directory
        dir.mkdir(exist_ok=True, parents=True)
        chown(str(dir), self._uid, self._gid)

    def _mkdir_homedir_parent_(self, homedir):
        homedir.parents[0].mkdir(
            exist_ok=True,
            parents=True)


def main():
    entrypoint = EntryPoint()
    entrypoint.add_user()
    entrypoint.add_gopass()
    entrypoint.add_gpg()
    entrypoint.add_ssh()
    entrypoint.add_git()
    entrypoint.add_bit()
    entrypoint.add_mapping()
    entrypoint.add_gcloud()
    entrypoint.add_docker()
    entrypoint.forward_agents()
    subprocess.run(['tail', '-f', '/debug/takelage.log'])


if __name__ == "__main__":
    main()
