import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_hugo_configure_hugo_bash_completion(host, testvars):
    bash_completion_path = '/etc/bash_completion.d/hugo.sh'
    file = host.file(bash_completion_path)

    assert file.exists
    assert file.is_file
    assert file.mode == 0o644
