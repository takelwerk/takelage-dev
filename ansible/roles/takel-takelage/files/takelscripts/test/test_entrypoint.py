from argparse import Namespace
import logging
import os
import subprocess
import takelscripts
from textwrap import dedent
from pathlib import Path
from stat import filemode
from takelscripts.entrypoint import EntryPoint


def test_takelscripts_entrypoint_init_nodebug(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(debug=False))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    EntryPoint()

    assert '*******************************************' in caplog.text
    assert 'starting configuration:' in caplog.text


def test_takelscripts_entrypoint_init_debug(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(extra='.config/first:.config/second'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()

    output_args = \
        "command line arguments: " + \
        "Namespace(" + \
        "bit=False, " + \
        "debug=True, " + \
        "docker=False, " + \
        "docker_daemon_port=17873, " + \
        "extra='.config/first:.config/second', " + \
        "gid=1600, " + \
        "git=False, " + \
        "gopass=False, " + \
        "gpg=False, " + \
        "gpg_agent_port=17874, " + \
        "gpg_ssh_agent_port=17875, " + \
        "home='/home/testuser', " + \
        "runcmd='', " + \
        "ssh=False, " + \
        "uid=1500, " + \
        "username='testuser')"

    output_agent_forwards = \
        "agent_forwards: {" + \
        "'gpg-agent': " + \
        "{'path': '/home/testuser/.gnupg/S.gpg-agent', " + \
        "'port': 17874, " + \
        "'user': 'testuser', " + \
        "'group': 'testuser'}, " + \
        "'gpg-ssh-agent': " + \
        "{'path': '/home/testuser/.gnupg/S.gpg-agent.ssh', " + \
        "'port': 17875, " + \
        "'user': 'testuser', " + \
        "'group': 'testuser'}}"

    assert entrypoint._hostdir == Path('/hostdir')

    assert '*******************************************' in caplog.text
    assert 'starting configuration:' in caplog.text
    assert output_args in caplog.text
    assert "hostdir: /hostdir" in caplog.text
    assert output_agent_forwards in caplog.text


def test_takelscripts_entrypoint_add_bit_config(
        monkeypatch,
        caplog,
        tmp_path):
    homedir_config_path = tmp_path / 'hostdir/Library/Caches/Bit/config'
    homedir_config_path.mkdir(parents=True)
    homedir_config_file = homedir_config_path / 'config.json'
    homedir_config_file.touch()
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            bit=True,
            home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path / 'hostdir')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    entrypoint = EntryPoint()

    entrypoint.add_bit()

    bit_dir_logs = tmp_path / 'home/testuser/Library/Caches/Bit/logs'
    bit_dir_config = tmp_path / 'home/testuser/Library/Caches/Bit/config'

    expected_log_start = 'adding config: bit'
    expected_log_end = 'added config: bit'
    expected_log_dir_logs = 'creating homedir child directory: ' + \
                            str(bit_dir_logs)
    expected_log_dir_config = 'creating homedir child directory: ' + \
                              str(bit_dir_config)

    assert bit_dir_logs.is_dir()
    assert bit_dir_config.is_dir()

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text
    assert expected_log_dir_logs in caplog.text
    assert expected_log_dir_config in caplog.text


def test_takelscripts_entrypoint_add_bit_no_config(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            bit=True,
            home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path / 'hostdir')

    entrypoint = EntryPoint()

    entrypoint.add_bit()

    bit_dir_logs = tmp_path / 'home/testuser/Library/Caches/Bit/logs'
    bit_dir_config = tmp_path / 'home/testuser/Library/Caches/Bit/config'
    bit_file_config = bit_dir_config / 'config.json'

    expected_log_start = 'adding config: bit'
    expected_log_end = 'added config: bit'
    expected_log_dir_logs = 'creating homedir child directory: ' + \
                            str(bit_dir_logs)
    expected_log_dir_config = 'creating homedir child directory: ' + \
                              str(bit_dir_config)
    expected_log_file_config = 'creating bit config.json: ' + \
                               str(bit_dir_config) + '/config.json'

    assert bit_dir_logs.is_dir()
    assert bit_dir_config.is_dir()
    assert bit_file_config.is_file()

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text
    assert expected_log_dir_logs in caplog.text
    assert expected_log_dir_config in caplog.text
    assert expected_log_file_config in caplog.text


def test_takelscripts_entrypoint_add_docker(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            docker=True,
            home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()

    entrypoint.add_docker()

    docker_config_path = tmp_path / 'home/testuser/.docker'
    docker_config_file = docker_config_path / 'config.json'

    expected_log_start = 'adding config: docker'
    expected_log_end = 'added config: docker'
    # currently the entrypoint script creates a docker config only in case
    # the host has no config or uses osxkeychain to store password hashes
    # so this test should respect that... dunno how to test this right now..
    # expected_log_path = 'creating homedir child directory: ' + \
    #                     str(docker_config_path)
    #expected_log_file = 'creating docker config file: ' + \
    #                    str(docker_config_file)

    assert docker_config_path.is_dir()
    assert docker_config_file.is_file()

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text
    # assert expected_log_path in caplog.text
    # assert expected_log_file in caplog.text


def test_takelscripts_entrypoint_add_extra(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(extra='.config/first:.config/second'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    entrypoint = EntryPoint()

    entrypoint.add_extra()

    expected_log_start = 'adding config: extra'
    expected_log_end = 'added config: extra'

    expected_log_symlink1 = 'symlink: .config/first'
    expected_log_symlink2 = 'symlink: .config/second'

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text
    assert expected_log_symlink1 in caplog.text
    assert expected_log_symlink2 in caplog.text


def test_takelscripts_entrypoint_add_gopass_config(
        monkeypatch,
        caplog,
        tmp_path):
    gopass_config = dedent(f"""\
        autoclip: false
        autoimport: true
        cliptimeout: 45
        exportkeys: false
        mime: true
        nocolor: false
        nopager: false
        notifications: true
        path: {tmp_path}/home/testuser/.password-store
        safecontent: false
        mount 'my-passwords' => '{tmp_path}"""
                           """/home/testuser/.password-store-my-passwords'
                           """)

    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            gopass=True,
            home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path / 'hostdir')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_add_gopass_get_config_',
        lambda x: gopass_config)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    config = \
        """
        root:
          askformore: false
          autoclip: true
          autoprint: false
          autoimport: true
          autosync: false
          check_recipient_hash: false
          cliptimeout: 45
          concurrency: 1
          editrecipients: false
          nocolor: false
          noconfirm: true
          nopager: false
          notifications: true
          path: gpgcli-gitcli-fs+file://""" + str(
            tmp_path) + """/home/testuser/.password-store
          recipient_hash:
            .gpg-id: 1234567890
          safecontent: false
          usesymbols: false
        mounts:
          my-passwords:
            askformore: false
            autoclip: true
            autoprint: false
            autoimport: true
            autosync: true
            check_recipient_hash: false
            cliptimeout: 45
            concurrency: 1
            editrecipients: false
            nocolor: false
            noconfirm: true
            nopager: false
            notifications: true
            path: gpgcli-gitcli-fs+file://""" + str(
            tmp_path) + """/home/testuser/.password-store-my-passwords
            recipient_hash:
              .gpg-id: 5678901234
            safecontent: false
            usesymbols: false
        """

    hostdir_config_path = tmp_path / 'hostdir/.config/gopass'
    hostdir_config_path.mkdir(parents=True)

    hostdir_config_file = hostdir_config_path / 'config.yml'
    hostdir_config_file.write_text(config)

    entrypoint = EntryPoint()

    entrypoint.add_gopass()

    expected_log_start = 'adding config: gopass'
    expected_log_end = 'added config: gopass'

    expected_config_file = 'using gopass config file: ' + \
                           str(tmp_path) + \
                           '/hostdir/.config/gopass/config.yml'

    expected_log_symlink1 = 'symlink: .config/gopass'
    expected_log_symlink2 = 'symlink: .password-store'
    expected_log_symlink3 = 'symlink: .password-store-my-passwords'

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text

    assert expected_config_file in caplog.text

    assert expected_log_symlink1 in caplog.text
    assert expected_log_symlink2 in caplog.text
    assert expected_log_symlink3 in caplog.text


def test_takelscripts_entrypoint_add_gopass_noconfig(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            gopass=True,
            home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path / 'hostdir')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    entrypoint = EntryPoint()

    entrypoint.add_gopass()

    expected_log_start = 'adding config: gopass'
    expected_log_error = 'no gopass config file found'

    assert expected_log_start in caplog.text
    assert expected_log_error in caplog.text


def test_takelscripts_entrypoint_add_gpg(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            gpg=True,
            home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_copy_file_',
        log_arguments_copy_file)

    entrypoint = EntryPoint()

    entrypoint.add_gpg()

    expected_log_start = 'adding config: gpg'
    expected_log_end = 'added config: gpg'
    expected_log_chmod_gnupg = 'chmod 700 gnupg directory:'

    expected_log_symlink_file1 = 'symlink: .gnupg/pubring.kbx'
    expected_log_symlink_file2 = 'symlink: .gnupg/trustdb.gpg'
    expected_log_symlink_file3 = 'symlink: .gnupg/private-keys-v1.d'
    expected_log_symlink_file4 = 'symlink: .gnupg/openpgp-revocs.d'
    expected_log_symlink_file5 = 'symlink: .gnupg/crls.d'

    expected_log_copy_file1 = \
        "{'source': '/srv/.gnupg/dirmngr.conf', 'destination': '"
    expected_log_copy_file2 = \
        "{'source': '/srv/.gnupg/gpg-agent.conf', 'destination': '"
    expected_log_copy_file3 = \
        "{'source': '/srv/.gnupg/gpg.conf', 'destination': '"

    gnupg_dir = tmp_path / 'home/testuser/.gnupg'
    gnupg_dir_mode = os.stat(gnupg_dir).st_mode

    assert gnupg_dir.is_dir()
    assert gnupg_dir_mode == 16832

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text
    assert expected_log_chmod_gnupg in caplog.text

    assert expected_log_symlink_file1 in caplog.text
    assert expected_log_symlink_file2 in caplog.text
    assert expected_log_symlink_file3 in caplog.text
    assert expected_log_symlink_file4 in caplog.text
    assert expected_log_symlink_file5 in caplog.text

    assert expected_log_copy_file1 in caplog.text
    assert expected_log_copy_file2 in caplog.text
    assert expected_log_copy_file3 in caplog.text


def test_takelscripts_entrypoint_add_ssh(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(ssh=True))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    entrypoint = EntryPoint()

    entrypoint.add_ssh()

    expected_log_start = 'adding config: ssh'
    expected_log_end = 'added config: ssh'
    expected_log = 'symlink: .ssh'

    assert expected_log_start in caplog.text
    assert expected_log_end in caplog.text
    assert expected_log in caplog.text


def test_takelscripts_entrypoint_add_user(
        monkeypatch,
        caplog,
        tmp_path):
    uid = int(subprocess.run(
        ['id', '--user'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode('utf-8'))
    gid = int(subprocess.run(
        ['id', '--group'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode(
        'utf-8'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            gid=gid,
            home=str(tmp_path / 'home/testuser'),
            uid=uid))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_run_',
        log_argument)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_copy_file_',
        log_arguments_copy_file)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_create_group_',
        lambda x, y, z: Namespace(returncode=0))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_copy_takelage_yml_',
        lambda x: True)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_copy_bashrc_',
        lambda x: True)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_mkdir_bashrc_d_',
        lambda x: True)

    entrypoint = EntryPoint()

    entrypoint.add_user()

    expected_log_user = 'creating user: testuser'
    expected_log_grouos = 'adding user to groups: sudo,tty'
    expected_command_begin = \
        "['useradd', " \
        "'--create-home', " \
        "'--home-dir', "
    expected_command_end = \
        "'--groups', " \
        "'sudo,tty', " \
        "'--shell', " \
        "'/bin/bash', " \
        "'--non-unique', " \
        "'testuser']"
    expected_log_done = 'created user: testuser'

    assert (tmp_path / 'home').is_dir()

    assert expected_log_user in caplog.text
    assert expected_log_grouos in caplog.text
    assert expected_command_begin in caplog.text
    assert expected_command_end in caplog.text
    assert expected_log_done in caplog.text


def test_takelscripts_entrypoint_chown_home(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_run_',
        log_argument)

    entrypoint = EntryPoint()

    entrypoint.chown_home()

    command = \
        "['/bin/chown', " \
        "'--recursive', " \
        "'testuser.testuser', " \
        "'/home/testuser']"

    assert command in caplog.text


def test_takelscripts_entrypoint_docker_sock_group_permissions(
        monkeypatch,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_dockersockpath_',
        lambda x: tmp_path / 'docker.sock')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_dockersocketgroup_',
        lambda x, y: 'docker')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_add_user_to_group_',
        log_arguments_add_user_to_group)

    docker_sock = tmp_path / 'docker.sock'
    docker_sock.touch()

    entrypoint = EntryPoint()

    mode = docker_sock.stat().st_mode

    assert '-rw-r--r--' == filemode(mode)

    entrypoint.docker_sock_permissions()

    mode = docker_sock.stat().st_mode

    assert '-rw-rw-r--' == filemode(mode)


def test_takelscripts_entrypoint_forward_agents(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_run_and_fork_',
        log_argument)

    entrypoint = EntryPoint()

    entrypoint.forward_agents()

    first_forward_command = \
        "['/usr/bin/socat', " \
        "'UNIX-LISTEN:/home/testuser/.gnupg/S.gpg-agent," \
        "reuseaddr,fork,user=testuser,group=testuser', " \
        "'TCP:host.docker.internal:17874']"
    second_forward_command = \
        "['/usr/bin/socat', " \
        "'UNIX-LISTEN:/home/testuser/.gnupg/S.gpg-agent.ssh," \
        "reuseaddr,fork,user=testuser,group=testuser', " \
        "'TCP:host.docker.internal:17875']"

    assert first_forward_command in caplog.text
    assert second_forward_command in caplog.text


def test_takelscripts_entrypoint_chown_tty(
        monkeypatch,
        caplog,
        tmp_path):
    testfile = tmp_path / 'test'
    testfile.touch()
    uid = int(
        subprocess.run(
            ['id', '--user'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.decode('utf-8'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(uid=uid))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_run_',
        lambda x, y: Namespace(stdout=str(testfile).encode('utf-8')))

    entrypoint = EntryPoint()

    entrypoint.chown_tty()

    expected_log = 'readable and writeable for user'

    assert expected_log in caplog.text


def test_takelscripts_entrypoint_copy_takelage_yml_exists(
        monkeypatch,
        caplog,
        tmp_path):
    test_takelage_yml = tmp_path / '.takelage.yml'
    test_takelage_yml.touch()
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    entrypoint = EntryPoint()

    entrypoint._copy_takelage_yml_()

    symlink = 'symlink: .takelage.yml'

    assert symlink in caplog.text


def test_takelscripts_entrypoint_copy_takelage_yml_notexists(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)

    entrypoint = EntryPoint()

    entrypoint._copy_takelage_yml_()

    filename = '.takelage.yml'

    assert filename not in caplog.text


def test_takelscripts_entrypoint_copy_bashrc(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_copy_file_',
        log_arguments_copy_file)

    entrypoint = EntryPoint()

    entrypoint._copy_bashrc_()

    expected_log = \
        "{'source': '/root/.bashrc', 'destination': '/home/testuser/.bashrc'}"

    assert expected_log in caplog.text


def test_takelscripts_entrypoint_copy_file(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path / 'hostdir')

    entrypoint = EntryPoint()
    src = (tmp_path / 'src')
    src.touch()
    dest = (tmp_path / 'dest')
    entrypoint._copy_file_(src, dest)

    expected_log_begin = "copying file: {'source': '/"
    expected_log_middle = "/src', 'destination': '/"
    expected_log_end = "/dest'}"

    assert (tmp_path / 'dest').is_file()

    assert expected_log_begin in caplog.text
    assert expected_log_middle in caplog.text
    assert expected_log_end in caplog.text


def test_takelscripts_entrypoint_create_group(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_run_',
        log_argument)

    entrypoint = EntryPoint()

    entrypoint._create_group_('testuser', 1600)

    command = "['groupadd', " \
              "'--gid', " \
              "'1600', " \
              "'--non-unique', " \
              "'testuser']"

    expected_log = "creating group: {'name': 'testuser', 'gid': 1600}"

    assert command in caplog.text
    assert expected_log in caplog.text


def test_takelscripts_entrypoint_get_dockersocketgroup_exists(
        monkeypatch,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_dockersockpath_',
        lambda x: tmp_path / 'docker.sock')
    entrypoint = EntryPoint()

    docker_socket = tmp_path / 'docker.sock'
    docker_socket.touch()

    group = entrypoint._get_dockersocketgroup_(9999)

    assert docker_socket.group() == group


def test_takelscripts_entrypoint_get_dockersocketgroup_notexists_notcreate(
        monkeypatch,
        caplog):
    class dockersocketpath:
        def group():
            raise KeyError

    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_dockersockpath_',
        lambda x: dockersocketpath)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_group_exists_',
        lambda x, y: 0)
    entrypoint = EntryPoint()

    group = entrypoint._get_dockersocketgroup_(9999)

    unexpected_log = \
        "create_group: {'name': 'takelage_dockersock', 'gid': 9999}"

    assert group == 'takelage_dockersock'
    assert unexpected_log not in caplog.text


def test_takelscripts_entrypoint_get_dockersocketgroup_notexists_create(
        monkeypatch,
        caplog):
    class dockersocketpath:
        def group():
            raise KeyError

    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_dockersockpath_',
        lambda x: dockersocketpath)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_create_group_',
        log_arguments_create_group)
    entrypoint = EntryPoint()

    group = entrypoint._get_dockersocketgroup_(9999)

    expected_log = "create_group: {'name': 'takelage_dockersock', 'gid': 9999}"

    assert group == 'takelage_dockersock'
    assert expected_log in caplog.text


def test_takelscripts_entrypoint_mkdir_bashrc_d_exists(
        monkeypatch,
        caplog,
        tmp_path):
    bashrc_d_hostdir = tmp_path / '.bashrc.d'
    bashrc_d_hostdir.touch()
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_symlink_',
        log_argument_symlink)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path)

    entrypoint = EntryPoint()

    entrypoint._mkdir_bashrc_d_()

    expected_log = '.bashrc.d'

    assert expected_log in caplog.text


def test_takelscripts_entrypoint_mkdir_bashrc_d_notexists(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_mkdir_homedir_child_',
        log_argument)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path)

    entrypoint = EntryPoint()

    entrypoint._mkdir_bashrc_d_()

    expected_log = '.bashrc.d'

    assert expected_log in caplog.text


def test_takelscripts_entrypoint_mkdir_homedir_child(
        monkeypatch,
        caplog,
        tmp_path):
    uid = int(subprocess.run(
        ['id', '--user'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode(
        'utf-8'))
    gid = int(subprocess.run(
        ['id', '--group'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode(
        'utf-8'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            gid=gid,
            home=str(tmp_path / 'home/testuser'),
            uid=uid))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()
    entrypoint._mkdir_homedir_child_('tmp1/tmp2/tmp3')

    expected_log_begin = "creating homedir child directory: "
    expected_log_end = "/home/testuser/tmp1/tmp2/tmp3"

    assert (tmp_path / 'home/testuser/tmp1/tmp2/tmp3').is_dir()

    assert expected_log_begin in caplog.text
    assert expected_log_end in caplog.text


def test_takelscripts_entrypoint_mkdir_parent(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()
    entrypoint._mkdir_parents_(tmp_path / 'tmp1/tmp2/tmp3')

    expected_log_begin = "creating parent directory: "
    expected_log_end = "/tmp1/tmp2"

    assert (tmp_path / 'tmp1/tmp2').is_dir()
    assert not (tmp_path / 'tmp1/tmp2/tmp3').is_dir()

    assert expected_log_begin in caplog.text
    assert expected_log_end in caplog.text


def test_takelscripts_entrypoint_run(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()
    result = entrypoint._run_(['echo', '"banana"'])

    assert "banana" in result.stdout.decode('utf-8')

    assert 'running command: echo "banana"' in caplog.text


def test_takelscripts_entrypoint_run_and_fork(
        monkeypatch,
        tmp_path,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default())
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()
    entrypoint._run_and_fork_(['touch', str(tmp_path / 'test.txt')])

    expected_log_begin = "running command in background: touch /"
    expected_log_end = "/test.txt"

    assert (tmp_path / 'test.txt').exists

    assert expected_log_begin in caplog.text
    assert expected_log_end in caplog.text


def test_takelscripts_entrypoint_symlink(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(home=str(tmp_path / 'home/testuser')))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_hostdir_',
        lambda x: tmp_path / 'hostdir')

    entrypoint = EntryPoint()
    (tmp_path / 'hostdir').mkdir()
    (tmp_path / 'hostdir/.testconfig').touch()
    entrypoint._symlink_('.testconfig')

    expected_log_begin = "creating symlink: {'source': '/"
    expected_log_middle = "/hostdir/.testconfig', 'destination': '/"
    expected_log_end = "/home/testuser/.testconfig'}"

    assert (tmp_path / 'home/testuser/.testconfig').is_symlink()

    assert expected_log_begin in caplog.text
    assert expected_log_middle in caplog.text
    assert expected_log_end in caplog.text


def args_default(
        bit=False,
        debug=True,
        docker=False,
        extra='',
        gid=1600,
        git=False,
        gopass=False,
        gpg=False,
        home='/home/testuser',
        ssh=False,
        uid=1500):
    args = Namespace(
        bit=bit,
        debug=debug,
        docker=docker,
        docker_daemon_port=17873,
        extra=extra,
        gid=gid,
        git=git,
        gopass=gopass,
        gpg=gpg,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        home=home,
        runcmd='',
        ssh=ssh,
        uid=uid,
        username='testuser')
    return args


def log_argument(x, y):
    x._logger.debug(y)
    return Namespace(returncode=0)


def log_argument_symlink(x, y):
    x._logger.debug('symlink: ' + str(y))
    return Namespace(returncode=0)


def log_arguments_add_user_to_group(x, user, group):
    adduser = {'user': user, 'group': group}
    x._logger.debug(adduser)


def log_arguments_copy_file(x, src, dest):
    copy = {'source': str(src), 'destination': str(dest)}
    x._logger.debug(copy)


def log_arguments_create_group(x, name, gid):
    group = {'name': name, 'gid': gid}
    x._logger.debug('create_group: ' + str(group))


def mock_logger_init(x, debug):
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
