import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_packer_system_packer_version(host, testvars):
    takel_packer_version = str(testvars['takel_packer_version'])
    packer_version_output = \
        host.check_output('packer --version')
    packer_version_search = re.search(
        r'.*(\d{1,2}\.\d{1,2}\.\d{0,2}).*', packer_version_output)

    if packer_version_search is not None:
        assert packer_version_search.group(1) == takel_packer_version
    else:
        assert False, 'Unable to get packer version'
