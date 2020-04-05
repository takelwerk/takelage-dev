import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_docker_repository_apt_repository_key(host, testvars):
    key = testvars['takel_docker_ce_repository_key']
    command = f"apt-key adv --fetch-keys {key}"
    gpg_result = host.run(command)

    assert gpg_result.rc == 0

    if re.search(r'unchanged: 1', gpg_result.stderr):
        assert True
    else:
        assert False


def test_takel_docker_repository_apt_repository(host, testvars):
    docker_ce_repository = testvars['takel_docker_ce_repository']
    sources_list = host.file('sources.list.d/download_docker_com_linux_debian.list')

    assert docker_ce_repository == sources_list.content_string
