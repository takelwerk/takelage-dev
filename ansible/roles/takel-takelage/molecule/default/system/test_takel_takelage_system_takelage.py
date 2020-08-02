import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_system_takelage(host):
    command = 'cat /etc/takelage_version'
    takelage_version = host.run(command).stdout.strip("\n")

    command = '/usr/local/bin/takelage'
    output = host.run(command)
    expected = 'takelage: \x1b[32m' + takelage_version + '\x1b[00m'

    assert expected in output.stdout


def test_takel_takelage_system_takelage_summary(host):
    command = 'cat /etc/takelage_version'
    takelage_version = host.run(command).stdout.strip("\n")

    command = '/usr/local/bin/takelage --summary'
    output = host.run(command)
    expected = 'takelage: \x1b[32m' + takelage_version + '\x1b[00m'

    assert expected in output.stdout
