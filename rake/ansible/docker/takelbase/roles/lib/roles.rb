# frozen_string_literal: true

@cmd_ansible_docker_takelbase_test_roles_all = 'for dir in ' \
    '`find ansible/roles -maxdepth 2 -name molecule | sort`; ' \
    'do ' \
    'cd `dirname $dir`; ' \
    'molecule test; ' \
    'cd ../../../; ' \
    'done'

@cmd_ansible_docker_takelbase_test_roles_each = 'for dir in ' \
    '`find ansible/roles -maxdepth 2 -name molecule | sort`; ' \
    'do ' \
    'cd `dirname $dir`; ' \
    '(molecule test || exit); ' \
    'cd ../../../; ' \
    'done'

@cmd_ansible_docker_takelbase_role = "cd %<role_path>s && bash -c '" \
                                     "molecule %<command>s'"

@list_ansible_docker_takelbase_role = %i[converge destroy lint login test verify]
