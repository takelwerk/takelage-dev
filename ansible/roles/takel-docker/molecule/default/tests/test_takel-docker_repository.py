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
    repository_url = testvars['takel_docker_ce_repository_url']
    codename = testvars['takel_docker_ce_repository_codename']
    command = 'apt-cache policy'
    apt_policy = host.check_output(command)
    regex_pattern = \
        r".*500 " + re.escape(repository_url) + r" " + codename + r".*\n" + \
        r".*release.*o=(.*?),.*a=(.*?),.*l=(.*?),.*c=(.*?),.*" \
        + repository_url.split('/', 3)[2]

    regex_match = re.match(regex_pattern, apt_policy, re.DOTALL)
    if regex_match:
        assert regex_match.group(1) == 'Docker'
        assert regex_match.group(2) == codename
        assert regex_match.group(3) == 'Docker CE'
        assert regex_match.group(4) == 'stable'
    else:
        assert False
