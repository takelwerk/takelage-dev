import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_k3d_completion_dir(host, testvars):
    completion_dir = testvars['takel_k3d_completion_dir']
    dir = host.file(completion_dir)

    assert dir.exists
    assert dir.is_directory
    assert dir.user == 'root'
    assert dir.group == 'root'
    assert dir.mode == 0o755


def test_takel_k3d_k3d_bash_completion(host, testvars):
    completion_file = testvars['takel_k3d_k3d_bash_completion']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_k3d_kubectl_bash_completion(host, testvars):
    completion_file = testvars['takel_k3d_kubectl_bash_completion']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
