import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_k3d_install_packages_installed(host, testvars):
    takel_gpg_install_packages = \
        testvars['takel_k3d_deb_install_packages']

    for package in takel_gpg_install_packages:
        deb = host.package(package)

        assert deb.is_installed
