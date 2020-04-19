from argparse import Namespace
import takelscripts
from takelscripts.takelage import Takelage


def test_takelscripts_takelage_init(
        monkeypatch):
    args = Namespace(
        short=True)
    monkeypatch.setattr(
        takelscripts.takelage.Takelage,
        '_get_args_',
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
