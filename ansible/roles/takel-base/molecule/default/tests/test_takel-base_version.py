import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_version_file(host, testvars):
    version = testvars['takelage_project']['version']

    file = host.file('/etc/takelage_version')

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
    assert file.content_string == version
