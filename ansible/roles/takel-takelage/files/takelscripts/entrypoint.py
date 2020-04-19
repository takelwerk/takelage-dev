#!/usr/bin/env python3

import argparse
from builtins import FileNotFoundError
from datetime import datetime
from grp import getgrnam
import logging
from os import chown
from pathlib import Path
from shutil import copyfile
import subprocess
import yaml


class EntryPoint(object):

    def __init__(self):
        args = self._parse_args_()
        self._debug = args.debug
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._logger = self._logger_init_(self._debug)
        self._logger.info(
            '*******************************************')
        self._logger.info(
            'starting configuration: {now}'.format(
                now=now))
        self._bit = args.bit
        self._docker = args.docker
        self._extra = args.extra
        self._gid = args.gid
        self._extra = args.extra
        self._git = args.git
        self._gopass = args.gopass
        self._gpg = args.gpg
        self._ssh = args.ssh
        self._username = args.username
        self._uid = args.uid
        self._logger.debug(
            'command line arguments: {args}'.format(
                args=args))

        # homedir: home directory in docker container (/home/my_user)
        self._homedir = Path(args.home)

        # hostdir: host home directory mapped do docker container (/hostdir)
        self._hostdir = self._get_hostdir_()
        self._logger.debug(
            'hostdir: {hostdir}'.format(
                hostdir=self._hostdir))

        # gpg agent and gpg ssh agent which are tunneled
        # via socat from host to docker container
        self._agent_forwards = {
            'gpg-agent': {
                'path': str(self._homedir) + '/.gnupg/S.gpg-agent',
                'port': args.gpg_agent_port},
            'gpg-agent.ssh': {
                'path': str(self._homedir) + '/.gnupg/S.gpg-agent.ssh',
                'port': args.gpg_ssh_agent_port}}
        self._logger.debug(
            'agent_forwards: {agent_forwards}'.format(
                agent_forwards=self._agent_forwards))

    def add_bit(self):
        if not self._bit:
            return
        self._logger.debug(
            'adding config: bit')

        # bit directories
        self._mkdir_homedir_child_('Library/Caches/Bit/logs')
        self._mkdir_homedir_child_('Library/Caches/Bit/config')

        bit_config_file_hostdir = \
            self._hostdir / 'Library/Caches/Bit/config/config.json'
        bit_config_file_homedir = \
            self._homedir / 'Library/Caches/Bit/config/config.json'

        if bit_config_file_hostdir.exists():
            self._copy_file_(
                bit_config_file_hostdir,
                bit_config_file_homedir)
        else:
            self._logger.debug(
                'creating bit config.json: {file}'.format(
                    file=bit_config_file_homedir))
            bit_config_template = """
{"analytics_id":"40599udvk6jhxplr","analytics_reporting":false,"error_reporting":false}
"""
            bit_config_file_homedir.write_text(bit_config_template)

        self._logger.info('added config: bit')
        return True

    def add_docker(self):
        if not self._docker:
            return
        self._logger.debug(
            'adding config: docker')

        self._mkdir_homedir_child_('.docker')

        docker_config_file = self._homedir / '.docker/config.json'
        self._logger.debug(
            'creating docker config file: {file}'.format(
                file=str(docker_config_file)))
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
        docker_config_file.write_text(docker_config_template)
        chown(str(docker_config_file), self._uid, self._gid)

        self._logger.debug(
            'make docker.sock readable and writable for docker group')
        chown('/var/run/docker.sock', 0, getgrnam('docker').gr_gid)

        self._logger.info('added config: docker')
        return True

    def add_extra(self):
        if not self._extra:
            return False
        self._logger.debug(
            'adding config: extra')

        for item in self._extra.split(':'):
            self._symlink_(item)

        self._logger.info(
            'added config: extra')
        return True

    def add_git(self):
        if not self._git:
            return
        self._logger.debug(
            'adding config: git')

        self._copy_file_(
            self._hostdir / '.gitconfig',
            self._homedir / '.gitconfig')

        self._logger.info('added config: git')
        return True

    def add_gopass(self):
        if not self._gopass:
            return
        self._logger.debug(
            'adding config: gopass')

        gopass_config_file = self._hostdir / '.config/gopass/config.yml'

        try:
            gopass_config = yaml.safe_load(
                gopass_config_file.read_text(encoding='utf-8'))
        except FileNotFoundError:
            self._logger.warning(
                'no valid gopass config file found: {file}'.format(
                    file=str(gopass_config_file)))
            self._gopass = False
            return False

        self._symlink_('.config/gopass')

        # add path for the personal passwordstore
        if 'path' in gopass_config['root']:
            gopass_config_root_path = gopass_config['root']['path']
            root_path = Path(gopass_config_root_path.split(':', 1)[1])
            passwordstore_relpath = root_path.relative_to(self._homedir)
            self._symlink_(passwordstore_relpath)

        # add paths for mounted passwordstores
        for mount in gopass_config['mounts']:
            gopass_config_mount = gopass_config['mounts'][mount]
            if 'path' in gopass_config_mount:
                gopass_config_mount_path = gopass_config_mount['path']
                mount_path = Path(gopass_config_mount_path.split(':', 1)[1])
                passwordstore_relpath = mount_path.relative_to(self._homedir)
                self._symlink_(passwordstore_relpath)

        self._logger.info(
            'added config: gopass')
        return True

    def add_gpg(self):
        if not self._gpg:
            return
        self._logger.debug(
            'adding config: gpg')

        self._logger.debug(
            'create gnupg directory: {gpgdir}'.format(
                gpgdir=str(self._homedir / '.gnupg')))
        self._mkdir_homedir_child_('.gnupg')
        (self._homedir / '.gnupg').chmod(0o700)

        # files used from the host system
        gpg_links = [
            'pubring.kbx',
            'trustdb.gpg',
            'private-keys-v1.d',
            'openpgp-revocs.d',
            'crls.d']

        for item in gpg_links:
            self._symlink_(Path('.gnupg') / item)

        # files ignored from the host system
        gpg_copy = [
            'dirmngr.conf',
            'gpg-agent.conf',
            'gpg.conf']

        for item in gpg_copy:
            self._copy_file_(
                Path('/srv') / '.gnupg' / item,
                self._homedir / '.gnupg' / item)

        self._logger.info(
            'added config: gpg')
        return True

    def add_ssh(self):
        if not self._ssh:
            return
        self._logger.debug(
            'adding config: ssh')

        self._symlink_('.ssh')

        self._logger.info(
            'added config: ssh')
        return True

    def add_user(self):
        self._logger.debug(
            'creating user: {user}'.format(
                user=self._username))

        self._mkdir_parent_(self._homedir)

        group = {'name': self._username, 'gid': self._gid}
        self._logger.debug(
            'creating group: {group}'.format(
                group=group))
        command = ['groupadd',
                   '--gid', str(self._gid),
                   '--non-unique',
                   self._username]
        result = self._run_(command)
        if result.returncode:
            return False

        groups = 'sudo,tty'
        if self._docker:
            groups += ',docker'
        self._logger.debug(
            'adding user to groups: {groups}'.format(
                groups=groups))

        command = [
            'useradd',
            '--create-home',
            '--home-dir', str(self._homedir),
            '--gid', str(self._gid),
            '--uid', str(self._uid),
            '--groups', groups,
            '--shell', '/bin/bash',
            '--non-unique',
            self._username]
        result = self._run_(command)
        if result.returncode:
            return False

        # cp /hostdir/.takelage.yml ~/.takelage.yml
        takelage_yml_hostdir = self._hostdir / '.takelage.yml'
        if takelage_yml_hostdir.exists():
            takelage_yml_homedir = self._homedir / '.takelage.yml'
            self._copy_file_(
                takelage_yml_hostdir,
                takelage_yml_homedir)

        # cp /root/.bashrc ~/.bashrc
        self._copy_file_(
            Path('/root/.bashrc'),
            self._homedir / '.bashrc')

        # mkdir ~/.bashrc.d
        self._mkdir_homedir_child_('.bashrc.d')

        # tty
        command = ['tty']
        tty_device = self._run_(command).stdout.decode('utf-8').strip('\n')
        self._logger.debug('making tty readable and writeable for user')
        chown(tty_device, self._uid, -1)

        self._logger.info(
            'created user: {user}'.format(
                user=self._username))
        return True

    def chown_home(self):
        self._logger.debug(
            'changing ownership: {home}'.format(
                home=self._homedir))

        command = [
            '/bin/chown',
            '--recursive',
            '{user}.{group}'.format(
                user=self._username,
                group=self._username),
            str(self._homedir)]
        result = self._run_(command)
        if result.returncode:
            return False

        self._logger.info(
            'changed ownership: {home}'.format(
                home=self._homedir))
        return True

    def forward_agents(self):
        self._logger.debug(
            'forwarding agents')

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
            self._run_and_fork_(command)

        self._logger.info(
            'forwarded agents')
        return True

    def _copy_file_(self, src, dest):
        copy = {'source': str(src), 'destination': str(dest)}
        self._logger.debug(
            'copying file: {copy}'.format(
                copy=copy))
        copyfile(src, dest)

    def _get_hostdir_(self):
        return Path('/hostdir')

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
        directory = self._homedir / directory
        if not directory.exists():
            self._logger.debug(
                'creating homedir child directory: {directory}'.format(
                    directory=directory))
            directory.mkdir(parents=True)
            chown(str(directory), self._uid, self._gid)

    def _mkdir_parent_(self, dir):
        parentdir = dir.parents[0]
        if not parentdir.exists():
            self._logger.debug(
                'creating parent directory: {parentdir}'.format(
                    parentdir=parentdir))
            parentdir.mkdir(parents=True)

    def _parse_args_(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Set debug flag")
        parser.add_argument(
            "--gid",
            type=int,
            help="Group ID of the username used in the host system")
        parser.add_argument(
            "--gpg_agent_port",
            type=int,
            default=17874,
            help="Port of gpg agent socket")
        parser.add_argument(
            "--gpg_ssh_agent_port",
            type=int,
            default=17875,
            help="Port of gpg ssh agent socket")
        parser.add_argument(
            "--extra",
            type=str,
            default="",
            help="Colon-separated config files that should be symlinked")
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
            "--no-extra",
            dest="extra",
            action="store_false",
            default=True,
            help="Do not add extra configuation")
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

    def _run_(self, command):
        self._logger.debug(
            'running command: {command}'.format(
                command=' '.join(command)))
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        if result.returncode:
            'command failed: {command}'.format(
                command=' '.join(command))
            self._logger.debug(
                '  returncode: {returncode}'.format(
                    returncode=result.returncode))
            self._logger.debug(
                '  stdout: {stdout}'.format(
                    stdout=result.stdout))
            self._logger.debug(
                '  stderr: {stderr}'.format(
                    stderr=result.stderr))
        return result

    def _run_and_fork_(self, command):
        self._logger.debug(
            'running command in background: {command}'.format(
                command=' '.join(command)))
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    def _symlink_(self, item):
        src = self._hostdir / item
        dest = self._homedir / item
        self._mkdir_parent_(dest)
        symlink = {'source': str(src), 'destination': str(dest)}
        self._logger.debug(
            'creating symlink: {symlink}'.format(
                symlink=symlink))
        dest.symlink_to(src)


def main():
    entrypoint = EntryPoint()
    entrypoint.add_user()
    entrypoint.add_gopass()
    entrypoint.add_gpg()
    entrypoint.add_ssh()
    entrypoint.add_git()
    entrypoint.add_bit()
    entrypoint.add_extra()
    entrypoint.add_docker()
    entrypoint.chown_home()
    entrypoint.forward_agents()
    subprocess.run(['tail', '-f', '/debug/takelage.log'])


if __name__ == "__main__":
    main()
