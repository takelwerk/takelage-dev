import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.mark.parametrize("userid", [500, 99, 1000],
                         ids=lambda uid: 'uid: ' + str(uid))
@pytest.mark.parametrize("groupid", [20, 21, 1000],
                         ids=lambda gid: 'gid: ' + str(gid))
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
              '--no-bit ' + \
              '--no-docker ' + \
              '--no-gcloud ' + \
              '--no-git ' + \
              '--no-gopass ' + \
              '--no-gpg ' + \
              '--no-ssh ' + \
              '--gpg_agent_port 17874 ' + \
              '--gpg_ssh_agent_port 17875'

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
