import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_hg_system_extension_hg_git(host, testvars):
    hg_version_output = host.check_output('hg version -v')

    assert 'hggit' in hg_version_output
