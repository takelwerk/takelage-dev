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
        if 'skip_version_check' in package and package['skip_version_check']:
            continue

        # do not check dependency meta packages
        if "[" in package['name']:
            continue

        if 'alias' in package:
            package_name = package['alias']
        else:
            package_name = package["name"]

        # derive import name from package name
        dirstr = 'import pkg_resources; ' \
                 'print(pkg_resources.get_distribution(' \
                 f"'{package_name}').egg_info)"
        importstr = f"cat $(python3 -c \"{dirstr}\")/top_level.txt | tail -1"
        package_import = host.check_output(importstr)

        assert host.run_test(f"{python3} -c 'import {package_import}'"), \
            f"Failed to import {package['name']}"

        if 'version' not in package.keys() or \
                str(package['version']) == 'latest':
            continue

        installed_version = host.check_output(
            f"{python3} -c 'import {package_import}; "
            f"print({package_import}.__version__)'")
        assert str(package['version']) in str(installed_version), \
            (f"Expected version for {package['name']} is "
             f"{package['version']}, but {str(installed_version)}"
             " is installed")
