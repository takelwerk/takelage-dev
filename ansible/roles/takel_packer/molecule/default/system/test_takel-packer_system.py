import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_packer_system_packer_version(host, testvars):
    packer_version_output = \
        host.check_output('packer --version')
    packer_version_search = re.search(
        r'.*(\d{1,2}\.\d{1,2}\.\d{0,2}).*', packer_version_output)

    assert packer_version_search is not None, 'Unable to get packer version'
