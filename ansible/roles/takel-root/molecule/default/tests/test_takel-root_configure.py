import takeltest

testinfra_hosts = takeltest.hosts()


def test_geospin_root_configure_bashrc(host):
    file = host.file('/root/.bashrc')
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0o644'


def test_geospin_root_configure_vimrc(host):
    assert 'syntax on' in host.file('/root/.vimrc').content_string
    assert 'set number' in host.file('/root/.vimrc').content_string
