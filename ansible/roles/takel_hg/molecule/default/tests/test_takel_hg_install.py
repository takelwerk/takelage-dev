import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_hg_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_hg_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


def test_takel_hg_install_pip_packages(host, testvars):
    pip_packages = testvars['takel_hg_pip_packages']
    pip3_list_output = host.check_output('pip3 list')
    for pip_package in pip_packages:
        assert pip_package['name'] in pip3_list_output
