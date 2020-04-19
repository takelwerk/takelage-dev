from argparse import Namespace
import logging
import subprocess
import takelscripts
from takelscripts.entrypoint import EntryPoint


def test_takelscripts_entrypoint_init_nodebug(
        monkeypatch,
        caplog):
    args = Namespace(
        debug=False,
        gid=1600,
        home='/home/testuser',
        bit=False,
        docker=False,
        extra='',
        gcloud=False,
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args)
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
    args = Namespace(
        debug=True,
        gid=1600,
        home='/home/testuser',
        bit=False,
        docker=False,
        extra='.config/first:.config/second',
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    EntryPoint()

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
    args = Namespace(
        debug=True,
        gid=gid,
        home=str(tmp_path / 'home/testuser'),
        bit=False,
        docker=False,
        extra='',
        gcloud=False,
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        ssh=False,
        uid=uid,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args)
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
    args = Namespace(
        debug=True,
        gid=1600,
        home=str(tmp_path / 'home/testuser'),
        bit=False,
        docker=False,
        extra='',
        gcloud=False,
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args)
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
    args = Namespace(
        debug=True,
        gid=1600,
        home='/home/testuser',
        bit=False,
        docker=False,
        extra='',
        gcloud=False,
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()
    result = entrypoint._run_(['echo', '"banana"'])

    assert "banana" in result.stdout.decode('utf-8')

    assert 'running command: echo "banana"' in caplog.text


def test_takelscripts_entrypoint_symlink(
        monkeypatch,
        caplog,
        tmp_path):
    args = Namespace(
        debug=True,
        gid=1600,
        home=str(tmp_path / 'home/testuser'),
        bit=False,
        docker=False,
        extra='',
        gcloud=False,
        git=False,
        gopass=False,
        gpg=False,
        gpg_agent_port=17874,
        gpg_ssh_agent_port=17875,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_parse_args_',
        lambda x: args)
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

    expected_log_begin = "creating symlink: {'source': '"
    expected_log_middle = "/hostdir/.testconfig', 'destination': '"
    expected_log_end = "/home/testuser/.testconfig'}"

    assert (tmp_path / 'home/testuser/.testconfig').is_symlink()

    assert expected_log_begin in caplog.text
    assert expected_log_middle in caplog.text
    assert expected_log_end in caplog.text


def mock_logger_init(x, debug):
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
