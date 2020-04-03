import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_install_packages_installed(host, testvars):
    takel_docker_deb_install_packages = \
        testvars['takel_docker_deb_install_packages']

    for package in takel_docker_deb_install_packages:
        deb = host.package(package)

        assert deb.is_installed
