import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_hugo_system_hugo_version(host, testvars):
    hugo_version = str(testvars['takel_hugo_hugo_version'])
    hugo_version_output = host.check_output('hugo version')
    hugo_version_search = re.search(
        r'.*(\d{1,2}\.\d{1,2}\.\d{0,2}).*', hugo_version_output)

    if hugo_version_search is not None:
        assert hugo_version_search.group(1) == hugo_version
    else:
        assert False, 'Unable to get hugo version'
