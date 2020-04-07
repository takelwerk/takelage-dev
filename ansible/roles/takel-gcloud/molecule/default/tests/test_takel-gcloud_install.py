import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_gcloud_install_packages_installed(host, testvars):
    takel_gcloud_install_packages = \
        testvars['takel_gcloud_deb_install_packages']

    for package in takel_gcloud_install_packages:
        deb = host.package(package)

        assert deb.is_installed


def test_takel_gcloud_install_gcloud_installed(host, testvars):
    installation_root = testvars['takel_gcloud_installation_root']
    takel_gcloud_bin_path = installation_root + '/google-cloud-sdk/bin/gcloud'
    file = host.file(takel_gcloud_bin_path)

    assert file.is_file
