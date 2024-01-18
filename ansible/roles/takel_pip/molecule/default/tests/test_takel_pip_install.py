import pytest
import re
import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_pip_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_pip_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


@pytest.fixture(scope='module', name='installed_pip_packages')
def get_packages(host, testvars):
    if 'takel_pip_venv_path' in testvars:
        takel_python_venv_path = \
            testvars['takel_pip_venv_path']
        return host.check_output(takel_python_venv_path + '/bin/pip3 list')
    else:
        return host.check_output('pip3 list')


def test_takel_pip_check_version(installed_pip_packages,
                                 testvars):
    expected_pip_packages = testvars['takel_pip_packages']
    for package in expected_pip_packages:

        # do not check dependency meta packages
        if "[" in package['name']:
            continue

        installed = re.search(package['name'] + r'\s+(.*)',
                              installed_pip_packages,
                              re.IGNORECASE)
        assert installed is not None, f"{package['name']} is not installed."
        if 'version' in package.keys() and str(package['version']) != 'latest':
            assert str(package['version']) == installed.group(1).strip(), (
                f"Expected version for {package['name']} is "
                f"{installed.group(1).strip()}, but {package['version']}"
                " is installed")
