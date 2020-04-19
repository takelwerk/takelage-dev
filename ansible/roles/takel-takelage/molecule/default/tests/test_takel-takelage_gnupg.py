import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_gnupg_gpg_config_files(host, testvars):
    takel_takelage_gpg_config_path = '/srv/.gnupg/'
    takel_takelage_gpg_config_files = \
        testvars['takel_takelage_gpg_config_files']

    assert host.file(takel_takelage_gpg_config_path).is_directory
    for conf in takel_takelage_gpg_config_files:
        assert host.file(takel_takelage_gpg_config_path + conf).is_file


def test_takel_takelage_gnupg_gpg_config_gpg_agent(host):
    gpg_agent_conf = '/srv/.gnupg/gpg-agent.conf'

    assert host.file(gpg_agent_conf).contains(
        'pinentry-program /usr/bin/pinentry-curses')
