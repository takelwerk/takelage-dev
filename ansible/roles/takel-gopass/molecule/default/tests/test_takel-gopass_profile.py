import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_gopass_profile_exists(host, testvars):
    profile_order = testvars['takel_gopass_profile_order']
    file = host.file('/etc/profile.d/'
                     f"{str(profile_order)}gopass")

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
