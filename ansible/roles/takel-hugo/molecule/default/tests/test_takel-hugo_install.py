import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_hugo_install_packages_installed(host, testvars):
    takel_gpg_install_packages = \
        testvars['takel_hugo_deb_install_packages']

    for package in takel_gpg_install_packages:
        deb = host.package(package)

        assert deb.is_installed


def test_takel_hugo_install_hugo_package_installed(host):
    deb = host.package('hugo')

    assert deb.is_installed
