import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.fixture(name='python3')
def get_pip_binry(host, testvars):
    if 'takel_pip_venv_path' in testvars:
        takel_python_venv_path = \
            testvars['takel_pip_venv_path']
        return takel_python_venv_path + '/bin/python3'
    else:
        return 'python3'


def test_takel_pip_system_check_version(host, testvars, python3):
    expected_pip_packages = testvars['takel_pip_packages']
    for package in expected_pip_packages:

        # do not check dependency meta packages
        if "[" in package['name']:
            continue

        if 'alias' in package:
            package_name = package['alias']
        else:
            package_name = package["name"]

        assert host.run_test(f"{python3} -c 'import {package_name}'"), \
            f"Failed to import {package['name']}"

        if str(package['version']) == 'latest' or (
                'skip_version_test' in package.keys() and
                package['skip_version_test']):
            continue

        installed_version = host.check_output(
            f"{python3} -c 'import {package_name}; "
            f"print({package_name}.__version__)'")
        assert str(package['version']) in str(installed_version), \
            (f"Expected version for {package['name']} is "
             f"{package['version']}, but {str(installed_version)}"
             " is installed")
