import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_configure_autocompletion(host, testvars):
    file = host.file('/root/.bashrc')
    autocompletion = testvars['takel_takelage_autocompletion']

    assert autocompletion in file.content_string
