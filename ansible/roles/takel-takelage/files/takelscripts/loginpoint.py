#!/usr/bin/env python3

import argparse
import pwd
import subprocess
from time import sleep


class LoginPoint(object):

    def __init__(self):
        self._su_bin = subprocess.run(
            ['which', 'su'],
            stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        self.args = self._get_args_()
        self._debug = self.args.debug
        self._username = self.args.username
        self._waitfor = self.args.waitfor

    def check_username(self):
        try:
            pwd.getpwnam(self._username)
            return True
        except KeyError:
            print('User ' + self._username + ' does not exist.')
            return False

    def login_to_container(self):
        cmd_login = self._get_cmd_login_()
        subprocess.run(cmd_login)

    def print_status(self):
        cmd_status = self._get_cmd_status_()
        subprocess.run(cmd_status)

    def wait_until_container_ready(self):
        processes = self._get_processes_()

        # wait until the entrypoint.py script has finished
        while self._waitfor not in processes:
            processes = self._get_processes_()
            if self._debug:
                print('Container not ready. Waiting...')
            sleep(0.5)

    def _get_args_(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Set debug flag")
        parser.add_argument(
            "--username",
            type=str,
            help="su to this username")
        parser.add_argument(
            "--waitfor",
            type=str,
            default="tail -f /debug/takelage.log",
            help="Wait for this command")
        return parser.parse_args()

    def _get_cmd_login_(self):
        command = [
            self._su_bin,
            self._username]
        return command

    def _get_cmd_status_(self):
        command = [
            self._su_bin,
            self._username,
            '--command']
        if self._debug:
            command.append('/usr/bin/python3 /debug/takelage.py')
        else:
            command.append('/usr/local/bin/takelage --short')
        return command

    def _get_processes_(self):
        command = [
            'ps',
            'a']
        processes = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.decode('utf-8')
        return processes


def main():
    loginpoint = LoginPoint()
    loginpoint.wait_until_container_ready()
    if not loginpoint.check_username():
        exit(1)
    loginpoint.print_status()
    loginpoint.login_to_container()


if __name__ == "__main__":
    main()
