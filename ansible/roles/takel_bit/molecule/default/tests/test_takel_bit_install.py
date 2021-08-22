import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_bit_install_packages_installed(host, testvars):
    takel_gpg_install_packages = \
        testvars['takel_bit_deb_install_packages']

    for package in takel_gpg_install_packages:
        deb = host.package(package)

        assert deb.is_installed
