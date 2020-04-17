from argparse import Namespace
import pwd
import takelscripts
from takelscripts.loginpoint import LoginPoint


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
        monkeypatch):
    def raise_keyerror():
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