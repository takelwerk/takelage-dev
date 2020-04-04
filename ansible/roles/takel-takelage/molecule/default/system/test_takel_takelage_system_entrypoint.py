import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.mark.parametrize("host_os", ['macos', 'linux'],
                         ids=lambda os: 'OS: ' + str(os))
@pytest.mark.parametrize("groupid", [20, 21, 1000],
                         ids=lambda gid: 'gid: ' + str(gid))
@pytest.mark.parametrize("userid", [500, 99, 1000],
                         ids=lambda uid: 'uid: ' + str(uid))
def test_takel_takelage_system_entrypoint(host,
                                                 host_os,
                                                 userid,
                                                 groupid):
    username = 'testuser'

    host.run('userdel ' + username)
    host.run('rm -rf /Users /home/*')

    command = '/entrypoint.py ' \
              '--username ' + username + ' ' \
              '--gid ' + str(groupid) + ' ' \
              '--uid ' + str(userid) + ' ' \
              '--hostsystem ' + host_os + ' ' \
              '--no-gpg ' \
              '--no-ssh ' \
              '--no-git ' \
              '--no-docker'
    assert host.run_test(command)

    if host_os is 'macos':
        assert host.file('/Users').is_directory
        assert host.file('/Users/' + username).is_directory
    if host_os is 'linux':
        assert host.file('/home/' + username).is_directory
