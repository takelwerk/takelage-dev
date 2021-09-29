import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_hg_configure_hggit_config(host, testvars):
    hgrcd_dir = testvars['takel_hg_hgrcd_dir']
    file = host.file(f"{hgrcd_dir}/hggit.rc")

    assert file.exists
    assert file.is_file
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644
