from argparse import Namespace
import takelscripts
from takelscripts.takelage import Takelage


def test_takelscripts_takelage_init(
        monkeypatch):
    args = Namespace(
        summary=True)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_parse_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_takelage_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_tau_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_gpg_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_ssh_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_gopass_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_git_',
        lambda x: x)

    takelage = Takelage()

    assert takelage.summary()


def test_takelscripts_takelage_print_status_git(
        monkeypatch,
        capsys):
    args = Namespace(
        summary=False)
    status_git = {
        'returncode': 0,
        'name': 'name',
        'email': 'email',
        'gpg-key': 'gpg-key'}
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_parse_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_takelage_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_tau_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_gpg_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_ssh_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_gopass_',
        lambda x: x)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_status_git_',
        lambda x: status_git)

    takelage = Takelage()
    takelage.print_status_git()

    captured = capsys.readouterr()

    expected = 'git config status: ' +\
               '\t\x1b[32mavailable\x1b[00m\ngit config:\n\t' + \
               'name: \t\t\x1b[34mname\x1b[00m\n\t' + \
               'e-mail: \t\x1b[34memail\x1b[00m\n\t' + \
               'gpg signingkey: \x1b[34mgpg-key\x1b[00m\n'

    assert expected == captured.out
