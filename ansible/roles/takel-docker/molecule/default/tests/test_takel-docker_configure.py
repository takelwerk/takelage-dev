import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_configure_completion(host, testvars):
    completion_path = testvars['takel_docker_completion_path']
    file = host.file(completion_path)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
