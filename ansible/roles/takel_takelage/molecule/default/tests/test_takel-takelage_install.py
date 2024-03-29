import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_takelage_install_packages_installed(host, testvars):
    takel_docker_deb_install_packages = \
        testvars['takel_takelage_deb_install_packages']

    for package in takel_docker_deb_install_packages:
        deb = host.package(package)

        assert deb.is_installed
