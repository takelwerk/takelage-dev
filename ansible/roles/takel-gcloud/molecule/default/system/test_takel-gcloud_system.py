import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_gcloud_system_gcloud_version(host, testvars):
    gcloud_binary = testvars['takel_gcloud_installation_root'] + '/google-cloud-sdk/bin/gcloud'
    gcloud_version_output = host.check_output(gcloud_binary + ' version')

    assert gcloud_version_output is not None
