import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_pip_system_check_version(host, testvars):
    expected_pip_packages = testvars['takel_pip_packages']
    for package in expected_pip_packages:
        assert host.run_test(f"python3 -c 'import {package['name']}'"), \
            f"Failed to import {package['name']}"
        installed_version = host.check_output(
            f"python3 -c 'import {package['name']}; "
            f"print({package['name']}.__version__)'")
        assert package['version'] == installed_version, \
            (f"Expected version for {package['name']} is {installed_version}, "
            f"but {package['version']}")
