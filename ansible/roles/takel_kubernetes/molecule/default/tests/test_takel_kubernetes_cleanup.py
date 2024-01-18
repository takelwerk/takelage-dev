import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_kubernetes_helm_tmp_targz(host, testvars):
    tmp_dir = testvars['takel_kubernetes_helm_tmp_dir']

    assert host.run_expect([2], f"ls {tmp_dir}/helm*")


def test_takel_kubernetes_helm_tmp_targz_dir(host, testvars):
    targz_dir = testvars['takel_kubernetes_helm_tmp_targz_dir']
    dir = host.file(targz_dir)

    assert not dir.exists
