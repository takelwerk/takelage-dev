from packaging import version
import re
import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_docker_system_docker_available(host):
    docker_version_expected = version.parse('19.x.y')
    docker_version_output = host.check_output('docker --version')

    # grep the docker version
    docker_version_search = re.search(
        r'Docker\ version\ (\d{1,2}\.\d{1,2}\.?\d{1,2}?).*',
        docker_version_output)

    if docker_version_search is not None:
        assert version.parse(docker_version_search.group(1)) > \
               docker_version_expected
    else:
        assert False, 'Unable to get docker version'
