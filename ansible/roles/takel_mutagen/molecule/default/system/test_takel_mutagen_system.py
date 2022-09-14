import takeltest
import re
import subprocess

testinfra_hosts = takeltest.hosts()


def test_takel_mutagen_system_mutagen_version(host, testvars):
    takel_mutagen_version = str(testvars['takel_mutagen_version'])
    mutagen_version_output = \
        host.check_output('mutagen version')
    mutagen_version_search = re.search(
        r'(\d{1,2}\.\d{1,2}\.\d{0,2})', mutagen_version_output)

    assert mutagen_version_search is not None, 'Unable to get mutagen version'

    if takel_mutagen_version == 'latest':
        command = '/usr/bin/curl -sL https://api.github.com/repos/mutagen-io/mutagen/releases/latest | /usr/bin/jq -r ".tag_name"'
        processes = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True)
        takel_mutagen_version = processes.stdout.split('v')[-1].strip()
    assert mutagen_version_search.group(1) == takel_mutagen_version, \
        'Unable to get mutagen version'
