from packaging import version
import pytest
import re
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.fixture(scope='module', name='pytest_file')
def put_pytest_file(host, moleculebook):
    pytest_file_path = '/tmp/test_pytest.py'
    pytest_file_content = """\
import pytest

def test_pytest():
    assert True
"""

    playbook = moleculebook.get()
    args = dict(content=pytest_file_content,
                dest=pytest_file_path,
                mode='0755')
    task = dict(action=dict(module='copy',
                            args=args))
    playbook['tasks'].append(task)
    moleculebook.set(playbook)
    moleculebook.run()

    pytest_file = host.file(pytest_file_path)

    assert pytest_file.exists
    assert pytest_file.is_file
    assert pytest_file.mode == 0o755
    assert pytest_file.content_string == pytest_file_content


@pytest.fixture(scope='module', name='pytest_output')
def get_pytest_output(host, pytest_file):
    return host.check_output('pytest /tmp/test_pytest.py')


def test_takel_pip_system_pytest_available(pytest_output):
    assert 'pytest' in pytest_output


def test_takel_pip_system_pytest_version(pytest_output, testvars):
    pip_packages = testvars['takel_pip_packages']
    pytest_package = \
        [package for package in pip_packages if package['name'] == 'pytest']
    pytest_version_expected = version.parse(pytest_package[0]['version'])
    pytest_version_search = re.search(
        r'.*pytest-(\d{1,2}\.\d{1,2}\.?\d{1,2}?).*',
        pytest_output,
        re.MULTILINE)

    if pytest_version_search is not None:
        pytest_version = version.parse(pytest_version_search.group(1))
        assert pytest_version == pytest_version_expected
    else:
        assert False, 'Unable to get pytest version'
