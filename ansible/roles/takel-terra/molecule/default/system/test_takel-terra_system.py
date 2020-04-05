import takeltest
import re

testinfra_hosts = takeltest.hosts()


def test_takel_terra_system_terraform_version(host, testvars):
    terraform_version = str(testvars['takel_terra_terraform_version'])
    terraform_version_output = \
        host.check_output('terraform --version')
    terraform_version_search = re.search(
        r'.*(\d{1,2}\.\d{1,2}\.\d{0,2}).*', terraform_version_output)

    if terraform_version_search is not None:
        assert terraform_version_search.group(1) == terraform_version
    else:
        assert False, 'Unable to get terraform version'


def test_takel_terra_system_terragrunt_version(host, testvars):
    terragrunt_version = str(testvars['takel_terra_terragrunt_version'])
    terragrunt_version_output = \
        host.check_output('terragrunt --version')
    terragrunt_version_search = re.search(
        r'.*(\d{1,2}\.\d{1,2}\.\d{0,2}).*', terragrunt_version_output)

    if terragrunt_version_search is not None:
        assert terragrunt_version_search.group(1) == terragrunt_version
    else:
        assert False, 'Unable to get terragrunt version'
