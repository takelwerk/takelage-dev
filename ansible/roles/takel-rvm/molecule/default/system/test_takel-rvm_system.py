import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rvm_system_rvm_available(host, testvars):
    rvm_user = testvars['takel_rvm_user']
    rvm_binary_path = testvars['takel_rvm_rvm_binary']
    with host.sudo(rvm_user):
        rvm_version_output = host.check_output(f"{rvm_binary_path} version")

    assert 'https://rvm.io' in rvm_version_output


def test_takel_rvm_system_ruby_available(host, testvars):
    rvm_user = testvars['takel_rvm_user']
    with host.sudo(rvm_user):
        rvm_version_output = host.check_output("ruby --version")

    assert '[x86_64-linux]' in rvm_version_output
