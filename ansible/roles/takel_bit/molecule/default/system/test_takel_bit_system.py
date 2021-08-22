from packaging import version
import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_nodejs_system_bvm_available(host, testvars):
    bvm_version_output = host.check_output('bvm --version')

    if bvm_version_output is not None:
        assert version.Version(bvm_version_output)
    else:
        assert False, 'Unable to get bvm version'


def test_takel_nodejs_system_bit_available(host, testvars):
    bit_version_output = host.check_output('bit --version')

    if bit_version_output is not None:
        assert version.Version(bit_version_output)
    else:
        assert False, 'Unable to get bit version'
