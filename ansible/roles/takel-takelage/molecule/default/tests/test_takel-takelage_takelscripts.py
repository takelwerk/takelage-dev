import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_takelscripts_entrypoint_script(host, testvars):
    takel_takelage_entrypoint_script = \
        testvars['takel_takelage_entrypoint_path'] + 'entrypoint.py'

    file = host.file(takel_takelage_entrypoint_script)
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755


def test_takel_takelage_takelscripts_loginpoint_script(host, testvars):
    takel_takelage_loginpoint_script = \
        testvars['takel_takelage_entrypoint_path'] + 'loginpoint.py'

    file = host.file(takel_takelage_loginpoint_script)
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755


def test_takel_takelage_takelscripts_takelage_script(host, testvars):
    file = host.file('/usr/local/bin/takelage')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755
