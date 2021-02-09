import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rvm_system_rvm_available(host, testvars):
    rvm_binary_path = testvars['takel_rvm_rvm_binary']
    rvm_version_output = host.check_output(f"{rvm_binary_path} version")

    assert 'https://rvm.io' in rvm_version_output
