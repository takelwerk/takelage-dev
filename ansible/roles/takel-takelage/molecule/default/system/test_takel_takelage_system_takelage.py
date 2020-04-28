import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_system_takelage(host):
    command = 'cat /etc/debian_version'
    debian_version = host.run(command).stdout.strip("\n")

    command = 'cp /etc/debian_version /etc/takelage_version'
    host.run(command)

    command = '/usr/local/bin/takelage --summary'
    output = host.run(command)
    expected = 'takelage: \x1b[32m' + debian_version + '\x1b[00m\n'

    assert expected in output.stdout


def test_takel_takelage_system_takelage_summary(host):
    command = 'cat /etc/debian_version'
    debian_version = host.run(command).stdout.strip("\n")

    command = 'cp /etc/debian_version /etc/takelage_version'
    host.run(command)

    command = '/usr/local/bin/takelage --summary'
    output = host.run(command)
    expected = 'takelage: \x1b[32m' + debian_version + '\x1b[00m\n'

    assert expected in output.stdout
