from argparse import Namespace
import logging
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
        git=False,
        gopass=False,
        gpg=False,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_mkdir_homedir_parent_',
        lambda x, y: y)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    EntryPoint()

    assert '' == caplog.text


def test_takelscripts_entrypoint_init_debug(
        monkeypatch,
        caplog):
    args = Namespace(
        debug=True,
        gid=1600,
        home='/home/testuser',
        bit=False,
        docker=False,
        git=False,
        gopass=False,
        gpg=False,
        ssh=False,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_mkdir_homedir_parent_',
        lambda x, y: y)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    EntryPoint()

    assert 'Starting configuration...' in caplog.text
    assert 'username: testuser' in caplog.text
    assert 'userid: 1500' in caplog.text
    assert 'groupid: 1600' in caplog.text
    assert 'homedir: /home/testuser' in caplog.text
    assert 'bit: False' in caplog.text
    assert 'debug: True' in caplog.text
    assert 'git: False' in caplog.text
    assert 'gopass: False' in caplog.text
    assert 'gpg: False' in caplog.text
    assert 'ssh: False' in caplog.text


def mock_logger_init(x, debug):
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
