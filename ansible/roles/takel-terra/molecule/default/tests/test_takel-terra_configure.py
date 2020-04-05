import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_terra_configure_terraform_bash_completion(host, testvars):
    bash_completion_path = \
        testvars['takel_terra_terraform_bash_completion_path']
    file = host.file(bash_completion_path)

    assert file.exists
    assert file.is_file
    assert file.mode == 0o644
