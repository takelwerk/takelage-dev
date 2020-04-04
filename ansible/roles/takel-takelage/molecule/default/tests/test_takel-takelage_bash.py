import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_bash_aliases(host, testvars):
    file = host.file('/etc/profile.d/bash_aliases.sh')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_takelage_bash_prompt(host, testvars):
    file = host.file('/etc/profile.d/bash_prompt.sh')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_takelage_bash_completion(host, testvars):
    file = host.file('/etc/profile.d/make_completion.sh')
    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
