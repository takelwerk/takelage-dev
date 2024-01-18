import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_kubernetes_completion_dir(host, testvars):
    completion_dir = testvars['takel_kubernetes_completion_dir']
    dir = host.file(completion_dir)

    assert dir.exists
    assert dir.is_directory
    assert dir.user == 'root'
    assert dir.group == 'root'
    assert dir.mode == 0o755


def test_takel_kubernetes_completion_k3d(host, testvars):
    if testvars['takel_kubernetes_k3d_install'] != 'true':
        return

    completion_file = testvars['takel_kubernetes_k3d_completion']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_kubernetes_completion_helm(host, testvars):
    if testvars['takel_kubernetes_helm_install'] != 'true':
        return

    completion_file = testvars['takel_kubernetes_helm_completion']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_kubernetes_completion_kubectl(host, testvars):
    if testvars['takel_kubernetes_kubectl_install'] != 'true':
        return

    completion_file = testvars['takel_kubernetes_kubectl_completion']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
