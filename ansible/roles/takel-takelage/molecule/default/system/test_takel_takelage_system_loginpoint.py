import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


# stop and fail if test is running for more the 60 seconds
@pytest.mark.timeout(60)
def test_takel_takelage_system_loginpoint(host):
    command = '/loginpoint.py --username nonexistinguser --waitfor PID'
    output = host.run(command)
    expected = "User nonexistinguser does not exist.\n"

    assert output.stdout == expected
