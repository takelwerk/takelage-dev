import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rvm_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_rvm_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


def test_takel_rvm_install_binary_available(host, testvars):
    rvm_user = testvars['takel_rvm_user']
    rvm_binary_path = testvars['takel_rvm_rvm_binary']
    rvm_binary = host.file(rvm_binary_path)

    assert rvm_binary.exists
    assert rvm_binary.is_file
    assert rvm_binary.user == 'rvm_user'
    assert rvm_binary.group == 'rvm_user'
    assert rvm_binary.mode == 0o755
    assert rvm_binary.exists
