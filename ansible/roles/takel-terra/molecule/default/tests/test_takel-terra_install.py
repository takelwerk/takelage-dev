import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_terra_install_packages_installed(host, testvars):
    takel_gpg_install_packages = \
        testvars['takel_terra_deb_install_packages']

    for package in takel_gpg_install_packages:
        rpm = host.package(package)

        assert rpm.is_installed


def test_takel_terra_install_terraform_installed(host, testvars):
    terraform_bin = testvars['takel_terra_bin_path'] + '/terraform'
    file = host.file(terraform_bin)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755


def test_takel_terra_install_terragrunt_installed(host, testvars):
    terragrunt_bin = testvars['takel_terra_bin_path'] + '/terragrunt'
    file = host.file(terragrunt_bin)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o755
