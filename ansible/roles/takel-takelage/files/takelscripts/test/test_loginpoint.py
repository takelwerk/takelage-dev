from argparse import Namespace
import pwd
import takelscripts
from takelscripts.loginpoint import LoginPoint


def test_takelscripts_loginpoint_check_username_exists(
        monkeypatch):
    args = Namespace(
        debug=True,
        username='my_user',
        waitfor='tail -f /debug/takelage.log')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        'pwd.getpwnam',
        lambda x: x)
    loginpoint = LoginPoint()

    assert loginpoint.check_username()


def test_takelscripts_loginpoint_check_username_notexists(
        monkeypatch,
        capsys):
    def raise_keyerror(x):
        raise KeyError
    args = Namespace(
        debug=True,
        username='no_user',
        waitfor='tail -f /debug/takelage.log')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        'pwd.getpwnam',
        raise_keyerror)
    loginpoint = LoginPoint()

    assert not loginpoint.check_username()

    expected = "User no_user does not exist.\n"
    captured = capsys.readouterr()

    assert expected == captured.out


def test_takelscripts_loginpoint_wait_until_container_ready_nodebug(
        monkeypatch,
        capsys):
    def _get_processes_mock_(x, when):
        if (when == 'start'):
            return ''
        return 'my_process'
    args = Namespace(
        debug=False,
        username='my_user',
        waitfor='my_process')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_processes_',
        _get_processes_mock_)
    loginpoint = LoginPoint()
    loginpoint.wait_until_container_ready()
    captured = capsys.readouterr()
    expected = ''

    assert expected == captured.out


def test_takelscripts_loginpoint_wait_until_container_ready_debug(
        monkeypatch,
        capsys):
    def _get_processes_mock_(x, when):
        if (when == 'start'):
            return ''
        return 'my_process'
    args = Namespace(
        debug=True,
        username='my_user',
        waitfor='my_process')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_processes_',
        _get_processes_mock_)
    loginpoint = LoginPoint()
    loginpoint.wait_until_container_ready()
    captured = capsys.readouterr()
    expected = "Container not ready. Waiting...\n"

    assert expected == captured.out


def test_takelscripts_loginpoint_get_cmd_login(
        monkeypatch):
    args = Namespace(
        debug=False,
        username='my_user',
        waitfor='tail -f /debug/takelage.log')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    loginpoint = LoginPoint()
    cmd_login = loginpoint._get_cmd_login_()
    expected = [
        '/bin/su',
        'my_user']

    assert expected == cmd_login


def test_takelscripts_loginpoint_get_cmd_status_nodebug(
        monkeypatch):
    args = Namespace(
        debug=False,
        username='my_user',
        waitfor='tail -f /debug/takelage.log')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    loginpoint = LoginPoint()
    cmd_status = loginpoint._get_cmd_status_()
    expected = [
        '/bin/su',
        'my_user',
        '--command',
        '/usr/local/bin/takelage --short']

    assert expected == cmd_status


def test_takelscripts_loginpoint_get_cmd_status_debug(
        monkeypatch):
    args = Namespace(
        debug=True,
        username='my_user',
        waitfor='tail -f /debug/takelage.log')
    monkeypatch.setattr(
        takelscripts.loginpoint.LoginPoint,
        '_get_args_',
        lambda x: args)
    loginpoint = LoginPoint()
    cmd_status = loginpoint._get_cmd_status_()
    expected = [
        '/bin/su',
        'my_user',
        '--command',
        '/usr/bin/python3 /debug/takelage.py']

    assert expected == cmd_status
