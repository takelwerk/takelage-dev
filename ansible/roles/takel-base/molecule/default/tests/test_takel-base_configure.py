import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_base_configure_locale(host):
    file = host.file('/etc/default/locale')

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
