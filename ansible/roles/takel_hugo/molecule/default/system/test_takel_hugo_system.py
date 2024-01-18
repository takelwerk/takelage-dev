import takeltest
import re
import requests

testinfra_hosts = [takeltest.hosts()[0]]


def test_takel_hugo_system_hugo_version(host, testvars):
    takel_hugo_hugo_version = str(testvars['takel_hugo_hugo_version'])
    hugo_version_output = \
        host.check_output('hugo version')
    hugo_version_search = re.search(
        r'.*(v\d{1,2}\.\d{1,3}\.\d{0,2}).*', hugo_version_output)

    assert hugo_version_search is not None, 'Unable to get hugo version'

    if takel_hugo_hugo_version == 'latest':
        url = "https://api.github.com/repos/gohugoio/hugo/releases/latest"
        response = requests.get(url)
        hugo_version = response.json()["tag_name"]
    assert hugo_version_search.group(1) == hugo_version, \
        'Unable to get hugo version'
