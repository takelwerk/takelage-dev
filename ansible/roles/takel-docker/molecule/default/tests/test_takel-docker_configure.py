import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_configure_completion_dir(host):
    completion_dir = '/etc/bash_completion.d'
    dir = host.file(completion_dir)

    assert dir.exists
    assert dir.is_directory
    assert dir.user == 'root'
    assert dir.group == 'root'
    assert dir.mode == 0o755


def test_takel_docker_configure_completion_file(host, testvars):
    completion_path = testvars['takel_docker_completion_path']
    file = host.file(completion_path)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
