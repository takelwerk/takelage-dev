import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_rvm_bash_completion(host, testvars):
    completion_file = testvars['takel_rvm_bash_completion']
    file = host.file(completion_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_takel_rvm_bash_completion_src(host, testvars):
    completion_src_parent = testvars['takel_rvm_completion_src_dir']
    completion_src_file = f"{completion_src_parent}/completion-ruby-all"
    file = host.file(completion_src_file)

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
