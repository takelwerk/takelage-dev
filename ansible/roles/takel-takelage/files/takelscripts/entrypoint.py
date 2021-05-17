#!/usr/bin/env python3

import argparse
import logging
import re
import subprocess
import shlex
import sys
from datetime import datetime
from os import chown, stat
from pathlib import Path
from shutil import copyfile
from stat import filemode, S_IRGRP, S_IWGRP


class EntryPoint(object):

    def __init__(self):
        args = self._parse_args_()
        print(args)
        self._debug = args.debug
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._logger = self._logger_init_(self._debug)
        self._logger.info('*******************************************')
        self._logger.info('starting configuration: {now}'.format(now=now))
        self._bit = args.bit
        self._docker = args.docker
        self._extra = args.extra
        self._gid = args.gid
        self._extra = args.extra
        self._git = args.git
        self._gopass = args.gopass
        self._gpg = args.gpg
        self._mutagen = args.mutagen
        self._ssh = args.ssh
        self._username = args.username
        self._uid = args.uid
        self._runcmd = args.runcmd
        self._logger.debug('command line arguments: {args}'.format(args=args))

        # homedir: home directory in docker container (/home/my_user)
        self._homedir = Path(args.home)

        # hostdir: host home directory mapped do docker container (/hostdir)
        self._hostdir = self._get_hostdir_()
        self._logger.debug('hostdir: {hostdir}'.format(hostdir=self._hostdir))

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
            self._symlink_('Library/Caches/Bit/config/config.json')
        else:
            self._logger.debug(
                'creating bit config.json: {file}'.format(
                    file=bit_config_file_homedir))
            bit_config_template = \
                '{"analytics_id":"40599udvk6jhxplr",' \
                '"analytics_reporting":false,' \
                '"error_reporting":false}\n'
            bit_config_file_homedir.write_text(bit_config_template)

        self._logger.info(
            'added config: bit')
        return True

    def add_docker(self):
        if not self._docker:
            return
        self._logger.debug(
            'adding config: docker')

        create_symlink = False
        docker_config_dir_hostdir = \
            self._hostdir / '.docker'
        docker_config_file_hostdir = \
            self._hostdir / '.docker/config.json'

        if docker_config_dir_hostdir.exists():
            create_symlink = True
            if docker_config_file_hostdir.exists():
                config = docker_config_file_hostdir.read_text()
                if 'osxkeychain' in config or 'desktop' in config:
                    self._logger.info(
                        'invalid docker credential helper found in ' +
                        f"'{docker_config_file_hostdir}': " +
                        'no synmlink to ' +
                        f"{docker_config_dir_hostdir} created")
                    create_symlink = False
        if docker_config_dir_hostdir.exists() and create_symlink:
            self._symlink_('.docker')
        else:
            self._mkdir_homedir_child_('.docker')
            docker_config_homedir = self._homedir / '.docker/config.json'
            self._logger.debug(
                'creating docker config file: {file}'.format(
                    file=str(docker_config_homedir)))
            docker_config_template = \
                '{\n' \
                '  "credHelpers": {\n' \
                '    "gcr.io": "gcloud",\n' \
                '    "us.gcr.io": "gcloud",\n' \
                '    "eu.gcr.io": "gcloud",\n' \
                '    "asia.gcr.io": "gcloud",\n' \
                '    "staging-k8s.gcr.io": "gcloud",\n' \
                '    "marketplace.gcr.io": "gcloud"\n' \
                '  }\n' \
                '}\n'
            docker_config_homedir.write_text(docker_config_template)

        self._logger.info(
            'added config: docker')
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

        gitconfig_hostdir = self._hostdir / '.gitconfig'
        if gitconfig_hostdir.exists():
            self._symlink_('.gitconfig')

        self._logger.info('added config: git')
        return True

    def add_gopass(self):
        if not self._gopass:
            return
        self._logger.debug('adding config: gopass')

        config_exists = self._add_gopass_config_file_()

        if not config_exists:
            return False

        gopass_config = self._add_gopass_get_config_()

        if not gopass_config:
            return False

        self._add_gopass_path_(gopass_config, '^path: (.*)$')

        self._add_gopass_path_(gopass_config, '^mount ".*?" => "(.*)"$')

        self._logger.info(
            'added config: gopass')
        return True

    def add_gpg(self):
        if not self._gpg:
            return
        self._logger.debug(
            'adding config: gpg')

        self._mkdir_homedir_child_('.gnupg')
        self._logger.debug(
            'chmod 700 gnupg directory: {gpgdir}'.format(
                gpgdir=str(self._homedir / '.gnupg')))
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

    def add_mutagen(self):
        if not self._mutagen:
            return
        self._logger.debug('adding config: mutagen')

        self._mkdir_homedir_child_('.mutagen/daemon')

        self._logger.info(
            'added config: mutagen')
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
            'creating user: {user}'.format(user=self._username))

        self._mkdir_parents_(self._homedir)

        result = self._create_group_(self._username, self._gid)
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

        self._copy_takelage_yml_()

        self._copy_bashrc_()

        self._mkdir_bashrc_d_()

        self._logger.info(
            'created user: {user}'.format(
                user=self._username))
        return True

    def chown_tty(self):
        self._logger.debug(
            'changing ownership: tty')
        command = ['tty']
        tty_device = self._run_(command).stdout.decode('utf-8').strip('\n')
        self._logger.debug(
            f"making '{tty_device}' readable and writeable for user")
        try:
            chown(tty_device, self._uid, -1)
            self._logger.info(
                'changed ownership: tty')
        except Exception as e:
            self._logger.warning(
                f"changed ownership of tty failed: {e}")

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

    def docker_sock_permissions(self):
        self._logger.debug(
            'make /var/run/docker.sock readable and writable for user')
        docker_socket = self._get_dockersockpath_()
        if not docker_socket.exists():
            self._logger.debug(
                '/var/run/docker.sock does not exist')
            return False

        # check /var/run/docker.sock
        gid = stat(docker_socket).st_gid
        docker_socket_group = self._get_dockersocketgroup_(gid)
        mode = docker_socket.stat().st_mode
        docker_socket_stat = {
            'group': docker_socket_group,
            'gid': gid,
            'mode': filemode(mode)}
        self._logger.info(
            '{docker_socket_path}: {docker_socket_stat}'.format(
                docker_socket_path=str(docker_socket),
                docker_socket_stat=docker_socket_stat))

        self._converge_docker_socket_group_permissions_(
            docker_socket,
            mode)

        self._add_user_to_group_(
            self._username,
            docker_socket_group)

        self._logger.debug(
            'made /var/run/docker.sock readable and writable for user')

    def runcmd(self):
        if not self._runcmd:
            return False

        self._logger.info(
            f"run command(s): '{self._runcmd}'")

        for cmd in self._runcmd.split(';'):
            result = self._run_(shlex.split(cmd))
            if result.returncode:
                self._logger.error(f"command '{cmd}'" +
                                   ' terminated with {result.returncode}')
                # stderr = result.stderr.decode('utf-8').strip('\n')
                self._logger.error(result.stderr.decode('utf-8').strip('\n'))
                sys.exit(result.returncode)

        self._logger.info(
            f"command(s) terminated: '{self._runcmd}'")
        return True

    def _add_gopass_config_file_(self):
        gopass_config_file = \
            self._hostdir / '.config/gopass/config.yml'

        if not gopass_config_file.exists():
            self._logger.warning(
                'no gopass config file found')
            self._gopass = False
            return False

        self._logger.debug(
            'using gopass config file: {config_file}'.format(
                config_file=gopass_config_file))

        relpath = gopass_config_file.relative_to(self._hostdir)
        self._symlink_(relpath.parents[0])
        return True

    def _add_gopass_get_config_(self):
        command = ['sudo', '-u', self._username, 'gopass', 'config']
        result = self._run_(command)
        if result.returncode:
            self._logger.warning(
                'no gopass config available')
            self._gopass = False
            return False

        return result.stdout.decode('utf-8').strip('\n')

    def _add_gopass_path_(self, gopass_config, pattern):
        for line in gopass_config.splitlines():
            match = re.search(pattern, line)
            if match is not None:
                path = match.group(1)
                relpath = Path(path).parents[0].relative_to(self._homedir)
                self._symlink_(relpath)

    def _add_user_to_group_(self, user, group):
        self._logger.debug(
            'adding user {user} to group {group}'.format(
                user=user,
                group=group))
        command = ['/usr/sbin/adduser', user, group]
        self._run_(command)

    def _converge_docker_socket_group_permissions_(self, docker_socket, mode):
        if not mode & S_IRGRP or not mode & S_IWGRP:
            command = ['/bin/chmod', 'g+rw', str(docker_socket)]
            self._run_(command)

    def _copy_takelage_yml_(self):
        # cp /hostdir/.takelage.yml ~/.takelage.yml
        takelage_yml_hostdir = self._hostdir / '.takelage.yml'
        if takelage_yml_hostdir.exists():
            self._symlink_('.takelage.yml')

    def _copy_bashrc_(self):
        # cp /root/.bashrc ~/.bashrc
        self._copy_file_(Path('/root/.bashrc'), self._homedir / '.bashrc')

    def _copy_file_(self, src, dest):
        copy = {'source': str(src),
                'destination': str(dest)}
        self._logger.debug(
            'copying file: {copy}'.format(
                copy=copy))
        copyfile(src, dest)

    def _create_group_(self, name, gid):
        group = {
            'name': name,
            'gid': gid}
        self._logger.debug(
            'creating group: {group}'.format(
                group=group))
        command = ['groupadd',
                   '--gid',
                   str(gid),
                   '--non-unique',
                   name]
        return self._run_(command)

    def _get_dockersocketgroup_(self, gid):
        # check group name of /var/run/docker.sock
        try:
            docker_socket_group = self._get_dockersockpath_().group()
        except KeyError:
            # else check group name 'takelage_dockersock'
            docker_socket_group = 'takelage_dockersock'
            if not self._group_exists_(docker_socket_group) == 0:
                # else create 'takelage_dockersock' with group id gid
                self._create_group_(docker_socket_group, gid)
        return docker_socket_group

    def _get_dockersockpath_(self):
        return Path('/var/run/docker.sock')

    def _get_hostdir_(self):
        return Path('/hostdir')

    def _group_exists_(self, group):
        self._logger.debug(
            'checking group: {group}'.format(group=group))
        command = ['getent', 'group', group]
        return self._run_(command).returncode

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

    def _mkdir_bashrc_d_(self):
        bashrcd_hostdir = self._hostdir / '.bashrc.d'
        if bashrcd_hostdir.exists():
            self._symlink_('.bashrc.d')
        else:
            self._mkdir_homedir_child_('.bashrc.d')

            profile_file = \
                self._homedir / '.bashrc.d/profile'
            profile_template = \
                'if [ -f /etc/profile ]; then\n' \
                '  . /etc/profile\n' \
                'fi\n'
            profile_file.write_text(profile_template)

    def _mkdir_homedir_child_(self, directory):
        directory = self._homedir / directory
        if not directory.exists():
            self._logger.debug(
                'creating homedir child directory: {directory}'.format(
                    directory=directory))
            directory.mkdir(parents=True)

    def _mkdir_parents_(self, dir):
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
            "--docker_daemon_port",
            type=int,
            default=17873,
            help="Port of docker daemon socket")
        parser.add_argument(
            "--gid",
            type=int,
            help="Group ID of the username used in the host system")
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
            "--no-mutagen",
            dest="mutagen",
            action="store_false",
            default=True,
            help="Do not add mutagen configuration")
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
        parser.add_argument(
            "--runcmd",
            type=str,
            default="tail -f /debug/takelage.log",
            help="Run given command at the end of the script")
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
        symlink = {
            'source': str(src),
            'destination': str(dest)}
        if dest.exists():
            self._logger.debug(
                'symlink already exists: {symlink}'.format(
                    symlink=symlink))
            return
        self._logger.debug(
            'creating symlink: {symlink}'.format(
                symlink=symlink))
        self._mkdir_parents_(dest)
        dest.symlink_to(src)


def main():
    entrypoint = EntryPoint()
    entrypoint.add_user()
    entrypoint.add_mutagen()
    entrypoint.add_gopass()
    entrypoint.add_gpg()
    entrypoint.add_ssh()
    entrypoint.add_git()
    entrypoint.add_bit()
    entrypoint.add_extra()
    entrypoint.add_docker()
    entrypoint.chown_tty()
    entrypoint.chown_home()
    entrypoint.docker_sock_permissions()
    entrypoint.runcmd()


if __name__ == "__main__":
    main()
