import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_kubernetes_install_packages_installed(host, testvars):
    takel_kubernetes_install_packages = \
        testvars['takel_kubernetes_deb_install_packages']

    for package in takel_kubernetes_install_packages:
        deb = host.package(package)

        assert deb.is_installed


def test_takel_kubernetes_install_k3d_installed(host, testvars):
    if testvars['takel_kubernetes_k3d_install'] != 'true':
        return

    bin_file = testvars['takel_kubernetes_k3d_bbin']
    file = host.file(bin_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755


def test_takel_kubernetes_install_helm_installed(host, testvars):
    if testvars['takel_kubernetes_helm_install'] != 'true':
        return

    bin_file = testvars['takel_kubernetes_helm_bbin']
    file = host.file(bin_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755


def test_takel_kubernetes_install_kubectl_installed(host, testvars):
    takel_kubernetes_kubectl_deb_install_package = \
        testvars['takel_kubernetes_kubectl_deb_install_package']

    for package in takel_kubernetes_kubectl_deb_install_package:
        deb = host.package(package)

        assert deb.is_installed
