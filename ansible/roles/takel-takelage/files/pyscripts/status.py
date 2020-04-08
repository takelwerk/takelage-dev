#!/usr/bin/env python3

from argparse import ArgumentParser
import re
import subprocess


class Status(object):
    _RED = '125'
    _GREEN = '46'
    _BLUE = '38'

    def __init__(self):
        self._args = self._parse_args_()
        self._gpg_status = self._get_gpg_status_()
        self._ssh_status = self._get_ssh_status_()
        self._gopass_status = self._get_gopass_status_()
        self._git_status = self._get_git_status_()

    def _display_colored_text_(self, color, text):
        colored_text = f'\033[38;5;{color}m{text}\033[00m'
        return colored_text

    def print_ssh_status(self):
        if self._ssh_status['returncode'] == 0:
            print('SSH-Agent status: \t' +
                  self._display_colored_text_(
                      self._GREEN, 'available'))
            if not self._args.short:
                print('Available SSH-Keys:')
                for key in self._ssh_status['keys']:
                    print('\t\t\t' + self._display_colored_text_(
                        self._BLUE, key))
                print('\n')
        else:
            print('SSH-Agent status: \t' +
                  self._display_colored_text_(
                      self._RED, 'not available'))

    def print_gpg_status(self):
        if self._gpg_status['returncode'] == 0:
            print('GPG-Agent status: \t' +
                  self._display_colored_text_(
                      self._GREEN, 'available'))
            if not self._args.short:
                print('Available GPG-Keys:')
                for key in self._gpg_status['keys']:
                    print('\t\t\t' + self._display_colored_text_(
                        self._BLUE, key))
                print('\n')
        else:
            print('GPG-Agent status: \t' +
                  self._display_colored_text_(
                      self._RED, 'not available'))

    def print_gopass_status(self):
        used_gpg_keys = []
        for key in self._gopass_status['keys']:
            for own_key in self._gpg_status['keys']:
                if key in own_key and own_key not in used_gpg_keys:
                    used_gpg_keys.append(own_key)
        if self._gopass_status['returncode'] == 0 and len(used_gpg_keys) > 0:
            print('Gopass cfg status: \t' +
                  self._display_colored_text_(
                      self._GREEN, 'available'))
            if not self._args.short:
                print('Used gpg-keys:')
                for key in used_gpg_keys:
                    print('\t\t\t' + self._display_colored_text_(
                        self._BLUE, key))
                print('\n')
        else:
            print('Gopass status: \t\t' +
                  self._display_colored_text_(
                      self._RED, 'not available'))

    def print_git_status(self):
        if self._git_status['returncode'] == 0:
            print('Git config status: \t' +
                  self._display_colored_text_(
                      self._GREEN, 'available'))
            if not self._args.short:
                print('Git config:')
                print('\tName: \t\t' +
                      self._display_colored_text_(
                          self._BLUE, self._git_status['name']))
                print('\tEmail: \t\t' +
                      self._display_colored_text_(
                          self._BLUE, self._git_status['mail']))
                print('\tGPG signingkey: ' +
                      self._display_colored_text_(
                          self._BLUE, self._git_status['gpg-key']))
                print('\n')
        else:
            print('Git-Config status: \t' +
                  self._display_colored_text_(
                      self._RED, 'not available'))

    def print_footnote(self):
        if self._args.short:
            print('For detailed information please run: status')

    def _get_ssh_status_(self):
        _ssh_status = {'returncode': None,
                       'keys': []}

        command = 'SSH_AUTH_SOCK=~/.gnupg/S.gpg-agent.ssh ssh-add -l'
        ssh_add_result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        _ssh_status['returncode'] = ssh_add_result.returncode
        if ssh_add_result.returncode == 0:
            ssh_keys_string = ssh_add_result.stdout.decode('utf-8').strip('\n')
            ssh_keys_list = ssh_keys_string.split('\n')
            _ssh_status['keys'] = ssh_keys_list

        return _ssh_status

    def _get_gpg_status_(self):
        gpg_status = {
            'returncode': None,
            'keys': []}

        subprocess.run(
            ['gpg', '--list-secret-keys'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

        command = ['gpg', '--list-secret-keys']
        gpg_list_result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        gpg_returncode = gpg_list_result.returncode

        if gpg_returncode == 0:
            gpg_keys_string = gpg_list_result.stdout.decode('utf-8')

            keys = re.findall(r'sec(.*)\n(.*)\nuid(.*)', gpg_keys_string)
            for key in keys:
                key_info = ''.join(
                    key[0].strip() + ': ' +
                    key[1].strip() + ' - ' + key[2].strip())
                gpg_status['keys'].append(key_info)

            if keys:
                key_id = keys[0][1].strip()
                command = ['bash -c "set -o pipefail && echo "test" | gpg --sign --local-user ' + key_id + '"']
                gpg_encrypt_result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)
                gpg_status['returncode'] = gpg_encrypt_result.returncode
            else:
                gpg_status['returncode'] = 1

        return gpg_status

    def _get_gopass_status_(self):
        _gopass_status = {'returncode': None,
                          'keys': []}

        command = ['gopass', 'recipients']
        gopass_add_result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        _gopass_status['returncode'] = gopass_add_result.returncode

        if gopass_add_result.returncode == 0:
            gopass_keys_string = gopass_add_result.stdout.decode('utf-8')
            keys = re.findall(r'0x(.*?) -', gopass_keys_string)
            _gopass_status['keys'] = keys
        else:
            print('stderr:')
            print(gopass_add_result.stderr)

        return _gopass_status

    def _get_git_status_(self):
        _git_status = {
            'returncode': -1,
            'name': None,
            'mail': None,
            'gpg-key': None}
        command = ['git', 'config', '--list']
        git_result = subprocess.run(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        if git_result.returncode == 0:
            result = git_result.stdout.decode('UTF-8')
            git_name_search = re.search(r'user\.name=(.*)', result)
            git_mail_search = re.search(r'user\.email=(.*)', result)
            git_gpg_search = re.search(r'user\.signingkey=(.*)', result)
            if git_mail_search is not None and git_mail_search.group(1) is not None:
                _git_status['mail'] = git_mail_search.group(1)
            if git_name_search is not None and git_name_search.group(1) is not None:
                _git_status['name'] = git_name_search.group(1)
            if git_gpg_search is not None and git_gpg_search.group(1) is not None:
                gpg_fingerprint = git_gpg_search.group(1)
                for key in self._gpg_status['keys']:
                    if gpg_fingerprint in key:
                        _git_status['gpg-key'] = key
            if _git_status['name'] is not None and _git_status['mail'] is not None:
                _git_status['returncode'] = 0
            return _git_status

    def _parse_args_(self):
        parser = ArgumentParser()
        parser.add_argument(
            "--short",
            dest="short",
            action="store_true",
            default=False,
            help="Display only the status.")
        return parser.parse_args()


def main():
    status = Status()
    status.print_ssh_status()
    status.print_gpg_status()
    status.print_gopass_status()
    status.print_git_status()
    status.print_footnote()


if __name__ == "__main__":
    main()
