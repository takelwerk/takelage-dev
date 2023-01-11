import takeltest
import re
import requests

testinfra_hosts = takeltest.hosts()


def test_takel_k3d_system_k3d_version(host, testvars):
    takel_k3d_k3d_version = str(testvars['takel_k3d_k3d_version'])
    k3d_version_output = \
        host.check_output('k3d version')
    k3d_version_search = re.search(
        r'.*(v\d{1,2}\.\d{1,3}\.\d{0,2}).*', k3d_version_output)

    assert k3d_version_search is not None, 'Unable to get k3d version'

    if takel_k3d_k3d_version == 'latest':
        url = "https://api.github.com/repos/k3d-io/k3d/releases/latest"
        response = requests.get(url)
        k3d_version = response.json()["tag_name"]
    assert k3d_version_search.group(1) == k3d_version, \
        'Unable to get k3d version'


def test_takel_k3d_system_kubectl_version(host, testvars):
    kubectl_version_output = \
        host.check_output('kubectl version --client')

    assert 'Client Version: ' in kubectl_version_output, \
        'Unable to run kubectl'
