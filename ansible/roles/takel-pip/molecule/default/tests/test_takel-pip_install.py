import pytest
import re
import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_pip_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_pip_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


@pytest.fixture(scope='module', name='packages')
def get_packages(host, testvars):
    return host.check_output('pip3 list')


def test_takel_pip_install_pip_packages_installed(packages, testvars):
    for package in testvars['takel_pip_packages']:
        if '[' not in package['name']:
            assert package['name'] in packages


def test_takel_pip_install_pip_packages_version(packages, testvars):
    for package in testvars['takel_pip_packages']:
        if '[' not in package['name']:
            search = re.search(package['name'] +
                               '.*?' +
                               package['version'],
                               packages)
            assert search is not None
