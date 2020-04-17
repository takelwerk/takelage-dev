from argparse import Namespace
import logging
import takelscripts
from takelscripts.entrypoint import EntryPoint


def test_takelscripts_entrypoint_init(
        monkeypatch,
        capsys):
    args = Namespace(
        debug=False,
        gid=1600,
        home='/testuser',
        bit=True,
        docker=True,
        git=True,
        gopass=True,
        gpg=True,
        ssh=True,
        uid=1500,
        username='testuser')
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_get_args_',
        lambda x: args)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_prepare_homedir_',
        lambda x, y: y)
    monkeypatch.setattr(
        takelscripts.entrypoint.EntryPoint,
        '_logger_init_',
        mock_logger_init)

    entrypoint = EntryPoint()

    expected = ""
    captured = capsys.readouterr()

    assert expected == captured.out


def mock_logger_init(x, debug):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
