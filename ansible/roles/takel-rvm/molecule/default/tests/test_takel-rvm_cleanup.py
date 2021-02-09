import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rvm_cleanup_installer_absent(host, testvars):
    rvm_installer_path = testvars['takel_rvm_rvm_installer']
    rvm_installer = host.file(rvm_installer_path)

    assert not rvm_installer.exists
