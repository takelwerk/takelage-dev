import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.mark.parametrize("userid", [500, 99, 1000],
                         ids=lambda uid: 'uid: ' + str(uid))
@pytest.mark.parametrize("groupid", [20, 21, 1000],
                         ids=lambda gid: 'gid: ' + str(gid))
# stop and fail if test is running for more the 60 seconds
@pytest.mark.timeout(60)
def test_takel_takelage_system_entrypoint(
        host,
        userid,
        groupid):
    host.run('userdel testuser')
    host.run('rm -rf /testhome')

    command = '/entrypoint.py ' + \
              '--username testuser ' + \
              '--uid ' + str(userid) + ' ' + \
              '--gid ' + str(groupid) + ' ' + \
              '--home /testhome/testuser ' + \
              '--no-docker ' + \
              '--no-git ' + \
              '--no-gopass ' + \
              '--no-gpg ' + \
              '--no-hg ' + \
              '--no-ssh ' + \
              '--runcmd ""'

    assert host.run_test(command)

    home = host.file('/testhome/testuser')
    assert home.exists
    assert home.is_directory
    assert home.uid == userid
    assert home.gid == groupid
    assert home.mode == 0o755

    user = host.user('testuser')
    assert user.uid == userid
    assert user.gid == groupid
    assert user.home == '/testhome/testuser'
    assert user.shell == '/bin/bash'
    assert 'sudo' in user.groups
