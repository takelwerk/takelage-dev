import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_gem_profile_files(host, testvars):
    profile_files = testvars['takel_gem_profile']
    for profile_file in profile_files:
        file = host.file('/etc/profile.d/' +
                         str(profile_file['order']) +
                         profile_file['file'])

        assert file.exists
        assert file.is_file
        assert file.user == 'root'
        assert file.group == 'root'
        assert file.mode == 0o644
