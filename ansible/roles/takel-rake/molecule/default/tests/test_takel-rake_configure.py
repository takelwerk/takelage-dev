import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rake_configure_bash_completion(host):
    file = host.file('/etc/profile.d/rake-completion.sh')

    assert file.exists
    assert file.is_file
    assert file.mode == 0o644
