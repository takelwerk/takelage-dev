import testaid

testinfra_hosts = testaid.hosts()


def test_takel_base_configure_locale(host):
    file = host.file('/etc/default/locale')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_base_configure_20auto_upgrades(host):
    file = host.file('/etc/apt/apt.conf.d/20auto-upgrades')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_base_configure_50unattended_upgrades(host):
    file = host.file('/etc/apt/apt.conf.d/50unattended-upgrades')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
