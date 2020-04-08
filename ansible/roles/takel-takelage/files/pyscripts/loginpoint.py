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
        self.args = self._get_args()
        self._debug = self.args.debug
        self._username = self.args.username
        self._waitfor = self.args.waitfor

    def get_logincommand(self):
        command = [
            self._su_bin,
            self._username,
            '--login']
        return command

    def get_statuscommand(self):
        command = [
            self._su_bin,
            self._username,
            '--command']
        if self._debug:
            command.append('/usr/bin/python3 /debug/status.py')
        else:
            command.append('/usr/local/bin/status --short')
        return command

    def _get_args(self):
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

    # find the last command from entrypoint.py
    # which keeps the docker container running
    ps_command = subprocess.run(
        ['ps', 'a'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # wait until the entrypoint.py script has finished
    while loginpoint._waitfor not in ps_command.stdout.decode('utf-8'):
        ps_command = subprocess.run(
            ['ps', 'a'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        if loginpoint._debug:
            print('Container not ready. Waiting...')
        sleep(0.5)

    try:
        pwd.getpwnam(loginpoint._username)
    except KeyError:
        print('User ' + loginpoint._username + ' does not exist.')
        exit(1)

    subprocess.run(loginpoint.get_statuscommand())
    subprocess.run(loginpoint.get_logincommand())


if __name__ == "__main__":
    main()
