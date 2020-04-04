import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_system_loginpoint(host):
    command = '/loginpoint.py --username nonexistinguser --waitfor PID'
    output = host.run(command)
    expected = "User nonexistinguser does not exist.\n"

    assert output.stdout == expected
