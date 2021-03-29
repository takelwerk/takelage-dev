# frozen_string_literal: true

require 'rake'

@cmd_image_project = {
  build: 'cd packer && packer build ' \
         "--var 'ansible_environment=%<project_environment>s' " \
         "--var 'ansible_playbook=%<project_playbook>s' " \
         "--var 'base_repo=#{@project['dockerhub_base_repo']}' " \
         "--var 'base_user=#{@project['dockerhub_base_user']}' " \
         "--var 'base_tag=latest' " \
         "--var 'local_user=#{@project['local_user']}' " \
         "--var 'target_repo=#{@project['name']}' " \
         "--var 'target_tag=%<project_environment>s' " \
         'templates/docker/takelbase/project/build_from_base.json',
  test: 'TAKELAGE_PROJECT_ENV=%<project_environment>s bash -c ' \
        "'cd ansible && molecule test --scenario-name image'",
  login: 'TAKELAGE_PROJECT_ENV=%<project_environment>s bash -c ' \
        "'cd ansible && molecule login --scenario-name image'",
  create: 'TAKELAGE_PROJECT_ENV=%<project_environment>s bash -c ' \
        "'cd ansible && molecule create --scenario-name image'",
  verify: 'TAKELAGE_PROJECT_ENV=%<project_environment>s bash -c ' \
        "'cd ansible && molecule verify --scenario-name image'",
  destroy: 'TAKELAGE_PROJECT_ENV=%<project_environment>s bash -c ' \
        "'cd ansible && molecule destroy --scenario-name image'"

}
