import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_hg_install_deb_packages_installed(host, testvars):
    install_packages = testvars['takel_hg_deb_install_packages']

    for install_package in install_packages:
        package = host.package(install_package)

        assert package.is_installed


def test_takel_hg_install_pip_package_dulwich(host, testvars):
    pip3_list_output = host.check_output('pip3 list')

    assert 'dulwich' in pip3_list_output


def test_takel_hg_install_hggit_repo(host, testvars):
    hg_extension_dir = testvars['takel_hg_extension_dir']
    file = host.file(f"{hg_extension_dir}/hg-git/.hg")

    assert file.exists
    assert file.is_directory
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755
