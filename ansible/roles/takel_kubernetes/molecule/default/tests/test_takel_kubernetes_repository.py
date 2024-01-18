import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_kubernetes_repository_google_keyfile(host, testvars):
    if testvars['takel_kubernetes_google_cloud_repository_install'] != 'true':
        return

    completion_file = \
        testvars['takel_kubernetes_google_cloud_repository_keyfile']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_kubernetes_repository_google_repofile(host, testvars):
    if testvars['takel_kubernetes_google_cloud_repository_install'] != 'true':
        return

    kubernetes_repository = \
        testvars['takel_kubernetes_google_cloud_repository']
    repository_filename = \
        testvars['takel_kubernetes_google_cloud_repository_filename']
    file = '/etc/apt/sources.list.d/' + repository_filename + '.list'
    sources_list = host.file(file)

    assert kubernetes_repository == sources_list.content_string.rstrip("\n")
