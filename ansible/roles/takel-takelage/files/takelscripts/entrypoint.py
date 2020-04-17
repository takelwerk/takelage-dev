#!/usr/bin/env python3

import argparse
from builtins import FileNotFoundError
from grp import getgrnam
import logging
from os import chown, system
from pathlib import Path
import re
import subprocess
import yaml


class EntryPoint(object):

    def __init__(self):
        self._get_bin()
        args = self._get_args()
        self._debug = args.debug
        self._bit = args.bit
        self._docker = args.docker
        self._git = args.git
        self._gopass = args.gopass
        self._gpg = args.gpg
        self._ssh = args.ssh
        self._username = args.username
        self._groupid = args.gid
        self._userid = args.uid
        self._host_homedir = Path('/homedir')
        self._homedir = Path(args.home)
        self._homedir.parents[0].mkdir(exist_ok=True, parents=True)
        self._mapping_directories = {}
        self._agent_forwards = {
            'gpg-agent': {'path': None,
                          'port': 20000},
            'gpg-agent.ssh': {'path': None,
                              'port': 20001},
            'gpg-agent.extra': {'path': None,
                                'port': 20002},
            'gpg-agent.browser': {'path': None,
                                  'port': 20003},
            'ssh-agent': {'path': None,
                          'port': 20100}}
        self._logger_init()
        self._logger.info('Starting configuration...')
        self._logger.info('username: ' + self._username)
        self._logger.info('userid: ' + str(self._userid))
        self._logger.info('groupid: ' + str(self._groupid))
        self._logger.info('homedir: ' + str(self._homedir))
        self._logger.info('bit: ' + str(self._bit))
        self._logger.info('debug: ' + str(self._debug))
        self._logger.info('git: ' + str(self._git))
        self._logger.info('gopass: ' + str(self._gopass))
        self._logger.info('gpg: ' + str(self._gpg))
        self._logger.info('ssh: ' + str(self._ssh))

    def add_bit(self):
        if not self._bit:
            return

        # bit directories
        self._mkdir_user('Library/Caches/Bit/logs')
        self._mkdir_user('Library/Caches/Bit/config')

        # bit config
        bit_config_template = """
{"analytics_id":"40599udvk6jhxplr","analytics_reporting":false,"error_reporting":false}
"""
        bit_config_file = \
            self._homedir / 'Library/Caches/Bit/config/config.json'
        bit_config_file.write_text(bit_config_template)

        # ~/takelage.yml
        self._mapping_directories['.takelage.yml'] = self._host_homedir

        self._logger.info('bit config added.')

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
        self._mkdir_user('.docker')
        docker_config_file = self._homedir / '.docker/config.json'
        docker_config_file.write_text(docker_config_template)
        chown(str(docker_config_file), self._userid, self._groupid)
        self._logger.info('docker config added.')

    def add_gcloud(self):
        gcloud_system_path = Path('/srv/gcloud')
        if gcloud_system_path.exists():
            self._mkdir_user('.config')
            gcloud_config_path = self._homedir / '.config/gcloud'
            gcloud_config_path.symlink_to(gcloud_system_path)
            self._logger.info('gcloud config added.')

    def add_git(self):
        if not self._git:
            return
        self._mapping_directories['.gitconfig'] = self._host_homedir
        self._logger.info('git config added.')

    def add_gopass(self):
        if not self._gopass:
            return
        gopass_config_path = self._host_homedir / '.config/gopass/config.yml'

        try:
            gopass_config = yaml.safe_load(
                gopass_config_path.read_text(encoding='utf-8'))
        except FileNotFoundError:
            self._logger.warning(
                'No gopass config file found: gopass is unavailable.')
            self._gopass = False
            return False

        # add config
        self._mkdir_user('.config')
        self._mapping_directories['.config/gopass'] = self._host_homedir

        # add path for the personal passwordstore
        if 'path' in gopass_config['root']:
            gopass_config_root_path = gopass_config['root']['path']
            root_path = Path(gopass_config_root_path.split(':', 1)[1])
            passwordstore_relpath = root_path.relative_to(self._homedir)
            self._mapping_directories[passwordstore_relpath] = \
                self._host_homedir

        # add paths for mountet passwordstores
        for mount in gopass_config['mounts']:
            gopass_config_mount = gopass_config['mounts'][mount]
            if 'path' in gopass_config_mount:
                gopass_config_mount_path = gopass_config_mount['path']
                mount_path = Path(gopass_config_mount_path.split(':', 1)[1])
                passwordstore_relpath = mount_path.relative_to(self._homedir)
                self._mapping_directories[passwordstore_relpath] = \
                    self._host_homedir
        self._logger.info('gopass config added.')
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

        self._mkdir_user('.gnupg')
        (self._homedir / '.gnupg').chmod(0o700)
        for item in gpg_links:
            self._mapping_directories[Path('.gnupg') / item] = \
                self._host_homedir

        # files should ignored from the host system
        self._mapping_directories[Path('.gnupg/gpg-agent.conf')] = Path('/srv')
        self._mapping_directories[Path('.gnupg/gpg.conf')] = Path('/srv')
        self._mapping_directories[Path('.gnupg/dirmngr.conf')] = Path('/srv')
        self._logger.info('gpg config added.')

    def add_mapping(self):
        for item, path in self._mapping_directories.items():
            (self._homedir / item).symlink_to(path / item)

        # make tty read/writeable for user
        tty_device = subprocess.run(
            'tty',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.decode('utf-8').strip('\n')

        chown(tty_device, self._userid, -1)
        if self._docker:
            chown('/var/run/docker.sock', 0, getgrnam('docker').gr_gid)
        self._logger.info('Directory mappings added.')

    def add_ssh(self):
        if not self._ssh:
            return
        self._mapping_directories['.ssh'] = self._host_homedir
        self._logger.info('ssh config added.')

    def add_user(self):
        self._logger.info('Create user %s' % self._username)
        if self._docker:
            groups = 'docker,sudo,tty'
        else:
            groups = 'sudo,tty'

        self._add_group()

        useradd_command = [
            'useradd',
            '--create-home',
            '--home-dir', str(self._homedir),
            '--gid', str(self._groupid),
            '--uid', str(self._userid),
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
        self._logger.info('User added.')

        # cp /root/.bashrc ~/.bashrc
        src = Path('/root/.bashrc')
        dest = self._homedir / '.bashrc'
        dest.write_text(src.read_text())

        # mkdir ~/.bashrc.d
        self._mkdir_user('.bashrc.d')

        return True

    def get_agent_sockets(self):
        for agent in self._agent_forwards:
            if 'gpg-agent' in str(agent):
                self._get_agent_sockets_gpg()

    def forward_agents(self):
        for agent in self._agent_forwards:
            if self._agent_forwards[agent]['path'] is None:
                continue
            if 'root' in self._agent_forwards[agent]['path']:
                root_socket_path = \
                    Path(self._agent_forwards[agent]['path'])
                user_socket_path = \
                    self._homedir / root_socket_path.relative_to('/root/')
            else:
                user_socket_path = \
                    self._agent_forwards[agent]['path']

            command = [
                self._socat_bin,
                'UNIX-LISTEN:' + str(user_socket_path) +
                ',reuseaddr,fork,user=' + self._username +
                ',gid=' + str(self._groupid),
                'TCP:host.docker.internal:' +
                str(self._agent_forwards[agent]['port'])]

            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

    def _add_group(self):
        groupadd_command = ['groupadd',
                            '--gid', str(self._groupid),
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

    def _get_agent_sockets_gpg(self):
        gpg_sockets = [
            r'agent-socket:(.*)',
            r'agent-ssh-socket:(.*)']
        command = [self._gpgconf_bin, '--list-dirs']

        gpg_path_list = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        gpg_path_list = gpg_path_list.stdout.decode('utf-8')
        for sock in gpg_sockets:
            gpg_agent_path_search = re.search(sock, gpg_path_list)
            if gpg_agent_path_search is not None and \
                    gpg_agent_path_search.group(1):
                socket_path = Path(gpg_agent_path_search.group(1))
                socket_name = socket_path.name
                command = \
                    'echo "export SSH_AUTH_SOCK=~/.gnupg/S.gpg-agent.ssh" > ' \
                    '/etc/profile.d/ssh_agent.sh'
                system(command)

                self._agent_forwards[socket_name.split('S.')[1]]['path'] = \
                    str(socket_path)

    def _get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Set debug flag.")
        parser.add_argument(
            "--username",
            type=str,
            help="Username used in the host system")
        parser.add_argument(
            "--uid",
            type=int,
            help="User ID of the username used in the host system")
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
        return parser.parse_args()

    def _get_bin(self):
        self._gpgconf_bin = subprocess.run(
            ['which', 'gpgconf'],
            stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        self._socat_bin = subprocess.run(
            ['which', 'socat'],
            stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        self._su_bin = subprocess.run(
            ['which', 'su'],
            stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    def _logger_init(self):
        self._logger = logging.getLogger(__file__)
        self._logger.setLevel(logging.INFO)
        if self._debug:
            self._logger.setLevel(logging.DEBUG)
        Path('/debug').mkdir(exist_ok=True)
        fh = logging.FileHandler('/debug/takelage.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        self._logger.addHandler(fh)

    def _mkdir_user(self, directory):
        dir = self._homedir / directory
        dir.mkdir(exist_ok=True, parents=True)
        chown(str(dir), self._userid, self._groupid)


def main():
    entrypoint = EntryPoint()
    entrypoint.add_user()
    entrypoint.add_gopass()
    entrypoint.add_gpg()
    entrypoint.add_ssh()
    entrypoint.add_git()
    entrypoint.add_bit()
    entrypoint.add_mapping()
    entrypoint.get_agent_sockets()
    entrypoint.forward_agents()
    entrypoint.add_gcloud()
    entrypoint.add_docker()
    subprocess.run(['tail', '-f', '/debug/takelage.log'])


if __name__ == "__main__":
    main()