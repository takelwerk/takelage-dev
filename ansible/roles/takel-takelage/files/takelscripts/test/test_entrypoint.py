from argparse import Namespace
import logging
from pathlib import Path
import subprocess
import takelscripts
from takelscripts.entrypoint import EntryPoint


def test_takelscripts_entrypoint_init_nodebug(
        monkeypatch,
        caplog):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            debug=False))
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
        lambda x: args_default(
            extra='.config/first:.config/second'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()

    assert entrypoint._hostdir == Path('/hostdir')

    assert '*******************************************' in caplog.text
    assert 'starting configuration:' in caplog.text
    assert "command line arguments: " + \
           "Namespace(" + \
           "bit=False, " + \
           "debug=True, " + \
           "docker=False, " + \
           "extra='.config/first:.config/second', " + \
           "gid=1600, " + \
           "git=False, " + \
           "gopass=False, " + \
           "gpg=False, " + \
           "gpg_agent_port=17874, " + \
           "gpg_ssh_agent_port=17875, " + \
           "home='/home/testuser', " + \
           "ssh=False, " + \
           "uid=1500, " + \
           "username='testuser')" in caplog.text
    assert "hostdir: /hostdir" in caplog.text
    assert "agent_forwards: " + \
           "{'gpg-agent': " + \
           "{'path': '/home/testuser/.gnupg/S.gpg-agent', " + \
           "'port': 17874}, " + \
           "'gpg-agent.ssh': " + \
           "{'path': '/home/testuser/.gnupg/S.gpg-agent.ssh', " + \
           "'port': 17875}}" in caplog.text


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
        stderr=subprocess.PIPE).stdout.decode('utf-8'))
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
        log_arguments)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_create_group_',
        lambda x: True)

    entrypoint = EntryPoint()

    entrypoint.add_user()

    assert (tmp_path / 'home/testuser').is_dir()

    #assert 'xxx' in caplog.text


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
        "reuseaddr,fork,user=testuser,gid=1600', " \
        "'TCP:host.docker.internal:17874']"
    second_forward_command = \
        "['/usr/bin/socat', " \
        "'UNIX-LISTEN:/home/testuser/.gnupg/S.gpg-agent.ssh," \
        "reuseaddr,fork,user=testuser,gid=1600', " \
        "'TCP:host.docker.internal:17875']"

    assert first_forward_command in caplog.text
    assert second_forward_command in caplog.text


def test_takelscripts_entrypoint_chown_tty(
        monkeypatch,
        caplog,
        tmp_path):
    testfile = tmp_path / 'test'
    testfile.touch()
    uid = int(subprocess.run(
        ['id', '--user'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode('utf-8'))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
            uid=uid))
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_run_',
        lambda x, y: Namespace(
            stdout=str(testfile).encode('utf-8')))

    entrypoint = EntryPoint()

    entrypoint.chown_tty()

    expected_log = 'making tty readable and writeable for user'

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
        log_argument)

    entrypoint = EntryPoint()

    entrypoint._copy_takelage_yml_()

    symlink = '.takelage.yml'

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
        log_argument)

    entrypoint = EntryPoint()

    entrypoint._copy_takelage_yml_()

    symlink = '.takelage.yml'

    assert symlink not in caplog.text


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
        log_arguments)

    entrypoint = EntryPoint()

    entrypoint._copy_bashrc_()

    expected_src = '/root/.bashrc'
    expected_dest = '/home/testuser/.bashrc'

    assert expected_src in caplog.text
    assert expected_dest in caplog.text


def test_takelscripts_entrypoint_copy_file(
        monkeypatch,
        caplog,
        tmp_path):
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args_default(
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

    entrypoint._create_group_()

    command = "['groupadd', " \
              "'--gid', " \
              "'1600', " \
              "'--non-unique', " \
              "'testuser']"

    expected_log = "creating group: {'name': 'testuser', 'gid': 1600}"

    assert command in caplog.text
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
        log_argument)
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
        stderr=subprocess.PIPE).stdout.decode('utf-8'))
    gid = int(subprocess.run(
        ['id', '--group'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode('utf-8'))
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
        lambda x: args_default(
            home=str(tmp_path / 'home/testuser')))
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
        lambda x: args_default(
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
        debug=True,
        extra='',
        gid=1600,
        home='/home/testuser',
        uid=1500):
    args = Namespace(
        bit=False,
        debug=debug,
        docker=False,
        extra=extra,
        gid=gid,
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        home=home,
        ssh=False,
        uid=uid,
        username='testuser')
    return args


def log_argument(x, y):
    x._logger.debug(y)
    return Namespace(returncode=0)


def log_arguments(x, y, z):
    x._logger.debug(y)
    x._logger.debug(z)


def mock_logger_init(x, debug):
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
