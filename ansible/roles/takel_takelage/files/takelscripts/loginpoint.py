#!/usr/bin/env python3

import argparse
import pwd
import subprocess
from time import sleep


class LoginPoint(object):

    def __init__(self):
        args = self._parse_args_()
        self._debug = args.debug
        self._username = args.username
        self._waitfor = args.waitfor

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

    def wait_until_container_ready(self):
        processes = self._get_processes_('start')

        # wait until the entrypoint.py script has finished
        while self._waitfor not in processes:
            processes = self._get_processes_('loop')
            if self._debug:
                print('Container not ready. Waiting...')
            sleep(0.5)

    def _get_cmd_login_(self):
        command = [
            '/bin/su',
            self._username]
        return command

    def _get_processes_(self, when):
        command = [
            'ps',
            'a']
        processes = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.decode('utf-8')
        return processes

    def _parse_args_(self):
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


def main():
    loginpoint = LoginPoint()
    loginpoint.wait_until_container_ready()
    if not loginpoint.check_username():
        exit(1)
    loginpoint.login_to_container()


if __name__ == "__main__":
    main()
