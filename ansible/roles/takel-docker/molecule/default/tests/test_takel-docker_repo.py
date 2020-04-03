import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_repo_file(host, testvars):
    takel_docker_apt_cache_policy_docker_repo = \
        'https://download.docker.com/linux/debian buster/stable amd64 Packages'

    apt_cache_policy = host.check_output('apt-cache policy')

    assert takel_docker_apt_cache_policy_docker_repo in apt_cache_policy
