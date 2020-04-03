import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_bash_completion(host, testvars):
    takel_docker_ce_completion_path = \
        testvars['takel_docker_ce_completion_path']

    assert host.file(takel_docker_ce_completion_path).is_file
