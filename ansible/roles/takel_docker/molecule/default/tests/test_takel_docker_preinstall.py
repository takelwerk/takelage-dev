import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_preinstall_packages_installed(host, testvars):
    takel_docker_deb_preinstall_packages = \
        testvars['takel_docker_deb_preinstall_packages']

    for package in takel_docker_deb_preinstall_packages:
        deb = host.package(package)

        assert deb.is_installed
