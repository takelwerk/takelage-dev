import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_packer_install_packages_installed(host, testvars):
    takel_packer_install_packages = \
        testvars['takel_packer_deb_install_packages']

    for package in takel_packer_install_packages:
        deb = host.package(package)

        assert deb.is_installed


def test_takel_packer_deb_preinstall_packages(host, testvars):
    takel_packer_install_packages = \
        testvars['takel_packer_deb_preinstall_packages']

    for package in takel_packer_install_packages:
        deb = host.package(package)

        assert deb.is_installed
