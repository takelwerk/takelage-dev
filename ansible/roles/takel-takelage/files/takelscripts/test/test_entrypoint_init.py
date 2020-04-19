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
        '_mkdir_parent_',
        lambda x, y: y)
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
        '_mkdir_parent_',
        lambda x, y: y)
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


def mock_logger_init(x, debug):
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
