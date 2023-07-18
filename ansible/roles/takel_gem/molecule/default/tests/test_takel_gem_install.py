import pytest
import re
import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_gem_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_gem_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


@pytest.fixture(scope='module', name='gems')
def get_gems(host, testvars):
    return host.check_output('gem list')


def test_takel_gem_install_gem_gems_installed(gems, testvars):
    for gem in testvars['takel_gem_gems']:
        assert gem['name'] in gems


def test_takel_gem_install_gem_gems_version(gems, testvars):
    for gem in testvars['takel_gem_gems']:
        if 'version' not in testvars.keys():
            continue
        search = re.search(gem['name'] + '.*?' + str(gem['version']), gems)
        assert search is not None
