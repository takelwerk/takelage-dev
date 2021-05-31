variable "ansible_connection" {
  type = string
  default = "docker"
}

variable "ansible_environment" {
  type = string
  default = "{{ ansible_environment }}"
}

variable "ansible_playbook" {
  type = string
}

variable "base_repo" {
  type = string
}

variable "base_tag" {
  type = string
  default = "latest"
}

variable "base_user" {
  type = string
}

variable "local_user" {
  type = string
}

variable "target_repo" {
  type = string
}

variable "target_tag" {
  type = string
  default = "latest"
}

variable "privileged" {
  type = string
  default = ""
}

variable "run_command" {
  type = string
  default = "/bin/cat"
}

locals {
  ansible_host = "${var.target_repo}"
}
