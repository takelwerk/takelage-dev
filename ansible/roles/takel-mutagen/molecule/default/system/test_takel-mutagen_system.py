import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_mutagen_system_mutagen_version(host, testvars):
    takel_mutagen_version = str(testvars['takel_mutagen_version'])
    mutagen_version_output = \
        host.check_output('mutagen version')
    mutagen_version_search = re.search(
        r'.*(\d{1,2}\.\d{1,2}\.\d{0,2}).*', mutagen_version_output)

    if mutagen_version_search is not None:
        assert mutagen_version_search.group(1) == takel_mutagen_version
    else:
        assert False, 'Unable to get mutagen version'
