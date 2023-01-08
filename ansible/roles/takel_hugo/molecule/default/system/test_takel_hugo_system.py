import takeltest
import re
import requests

testinfra_hosts = takeltest.hosts()


def test_takel_hugo_system_hugo_version(host):
    response = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest")
    hugo_version = response.json()["tag_name"]

    hugo_version_output = host.check_output('hugo version')
    hugo_version_search = re.search(
        r'.*(v\d{1,2}\.\d{1,3}\.\d{0,2}).*', hugo_version_output)

    if hugo_version_search is not None:
        assert hugo_version_search.group(1) == hugo_version
    else:
        assert False, 'Unable to get hugo version'
