import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rvm_rvm_binary_available(host, testvars):
    rvm_user = testvars['takel_rvm_user']
    rvm_binary_path = testvars['takel_rvm_rvm_binary']
    with host.sudo(rvm_user):
        rvm_binary_path_absolute = \
            host.check_output(f"readlink -f {rvm_binary_path}")
    rvm_binary = host.file(rvm_binary_path_absolute)

    assert rvm_binary.exists
    assert rvm_binary.is_file
    assert rvm_binary.user == rvm_user

    if rvm_user == 'root':

        assert rvm_binary.group == 'rvm'
        assert rvm_binary.mode == 0o775

    else:

        assert rvm_binary.group == rvm_user
        assert rvm_binary.mode == 0o755
