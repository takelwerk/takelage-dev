import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_takelage_profile_files(host, testvars):
    profile_files = testvars['takel_takelage_profile']
    for profile_file in profile_files:
        file = host.file('/etc/profile.d/' +
                         str(profile_file['order']) +
                         profile_file['file'])

        assert file.exists
        assert file.is_file
        assert file.user == 'root'
        assert file.group == 'root'
        assert file.mode == 0o644
