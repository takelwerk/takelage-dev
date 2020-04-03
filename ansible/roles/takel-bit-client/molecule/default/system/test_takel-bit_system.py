import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_bit_client_system_bit_version(host, testvars):
    takel_bit_client_version = str(testvars['takel_bit_client_version'])
    bit_version_output = \
        host.check_output('bit --version')
    bit_version_search = re.search(
        r'(\d{1,2}\.\d{1,2}\.?\d{0,2}).*', bit_version_output)

    if bit_version_search is not None:
        assert bit_version_search.group(1) == takel_bit_client_version
    else:
        assert False, 'Unable to get bit version'
