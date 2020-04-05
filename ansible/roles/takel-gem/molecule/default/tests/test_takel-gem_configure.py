import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_gem_configure_path_wrappers(host, testvars):
    file = '/root/.bashrc'
    rvm_wrappers_path = testvars['"PATH={{ takel_gem_rvm_wrappers_path }}:$PATH"']
    line = 'PATH=' + rvm_wrappers_path + ':$PATH'

    assert line in file.content_string
