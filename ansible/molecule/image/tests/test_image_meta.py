import takeltest
import pytest
import subprocess

testinfra_hosts = [takeltest.hosts()[0]]


def test_image_meta_env_exists(image_meta_data):
    assert image_meta_data['Config']['Env'] is not None


def test_image_meta_cmd(image_meta_data):
    assert image_meta_data['Config']['Cmd'] == ['/usr/bin/tail --follow /dev/null']


def test_image_meta_user(image_meta_data):
    assert image_meta_data['Config']['User'] == ''


@pytest.mark.parametrize('process, expected_args', [
    ('python3', 'python3 /entrypoint.py '
                '--username testuser '
                '--uid 1010 '
                '--gid 1010 '
                '--home /testhome/testuser '
                '--no-bit '
                '--no-docker '
                '--no-git '
                '--no-gopass '
                '--no-gpg '
                '--no-ssh'),
    ('tail',    'tail -f /debug/takelage.log')])
def test_container_process(host, process, expected_args):
    procs_present = False
    process_result = host.process.filter(user='root', comm=process)
    for proc in process_result:
        if proc.args == expected_args:
            procs_present = True
            break

    assert procs_present is True


def test_container_process_tail(host):
    successfully_login = False
    command = '/usr/bin/docker exec ' \
              '--tty molecule-takelage-dev-test-image-prod ' \
              '/loginpoint.py --username testuser'.split(' ')
    try:
        subprocess.run(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=0.5)
    except subprocess.TimeoutExpired:
        process_result = host.process.filter(user='root', comm='python3')
        for proc in process_result:
            if proc.args == 'python3 /loginpoint.py --username testuser':
                successfully_login = True
                host.run('kill %s' % proc.pid)

    assert successfully_login is True
