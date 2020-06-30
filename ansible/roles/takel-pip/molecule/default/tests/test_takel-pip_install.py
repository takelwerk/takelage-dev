import pytest
import re
import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_pip_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_pip_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


@pytest.fixture(scope='module', name='installed_pip_packages')
def get_packages(host, testvars):
    return host.check_output('pip3 list')

def test_takel_pip_check_version(installed_pip_packages,
                                        host,
                                        testvars):
    expected_pip_packages = testvars['takel_pip_packages']
    for package in expected_pip_packages:
        installed = re.search(package['name'] + r'\s+(.*)',
                              installed_pip_packages)
        if installed is not None:
            assert package['version'] == installed.group(1).strip()
        else:
            assert False, f"{package['name']} is not installed."
