import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_packer_install_packages_installed(host, testvars):
    takel_gpg_install_packages = \
        testvars['takel_packer_deb_install_packages']

    for package in takel_gpg_install_packages:
        rpm = host.package(package)

        assert rpm.is_installed


def test_takel_packer_install_packer_installed(host, testvars):
    takel_packer_bin_path = testvars['takel_packer_bin_path'] + '/packer'

    assert host.file(takel_packer_bin_path).is_file
