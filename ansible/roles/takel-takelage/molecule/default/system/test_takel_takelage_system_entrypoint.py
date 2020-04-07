import takeltest

testinfra_hosts = takeltest.hosts()

def test_takel_takelage_system_entrypoint(host):

    host.run('userdel testuser')
    host.run('rm -rf /testhome')

    command = '/entrypoint.py ' \
              '--username testuser ' \
              '--gid 1500 ' \
              '--uid 1600 ' \
              '--home /testhome/testuser ' \
              '--no-gpg ' \
              '--no-ssh ' \
              '--no-git ' \
              '--no-docker'

    assert host.run_test(command)

    home = host.file('/testhome/testuser')
    assert home.exists
    assert home.is_directory
    assert home.user == 'testuser'
    assert home.group == 'testuser'
    assert home.uid == 1500
    assert home.gid == 1600
    assert home.mode == 0o755

    user = host.user('testuser')
    assert user.uid == 1500
    assert user.gid == 1600
    assert user.home == '/testhome/testuser'
    assert user.shell == '/bin/bash'
    assert 'sudo' in user.groups
