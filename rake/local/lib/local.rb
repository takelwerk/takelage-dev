# frozen_string_literal: true

require 'rake'

@cmd_local_molecule_command = \
  'cd ansible && ' \
  'TAKELAGE_PROJECT_ENV=%<project_environment>s ' \
  'molecule %<molecule_command>s --scenario-name local'

@cmd_local_molecule_features = \
  'cd ansible && ' \
  'TAKELAGE_PROJECT_ENV=%<project_environment>s ' \
  'molecule dependency --scenario-name local'

@cmd_local_list = {
  converge: @cmd_local_molecule_command,
  destroy: @cmd_local_molecule_command,
  login: @cmd_local_molecule_command,
  verify: @cmd_local_molecule_command,
  features: @cmd_local_molecule_features
}
