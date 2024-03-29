packer {
  required_plugins {
    ansible = {
      version = "~> 1"
      source = "github.com/hashicorp/ansible"
    }
    docker = {
      source  = "github.com/hashicorp/docker"
      version = "~> 1"
    }
  }
}

source "docker" "takelage" {
  image = "${var.base_user}/${var.base_repo}:${var.base_tag}"
  commit = true
  pull = false
  run_command = "${local.run_command}"
  changes = [
    "CMD ${var.command}",
    "ENV DEBIAN_FRONTEND=noninteractive",
    "ENV LANG=en_US.UTF-8",
    "ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "LABEL mutagen=${var.mutagen}",
    "WORKDIR /root"
  ]
}

build {
  sources = [
    "source.docker.takelage"
  ]

  provisioner "ansible" {
    ansible_env_vars = [
      "ANSIBLE_HOST_KEY_CHECKING=False",
      "ANSIBLE_SSH_ARGS='-v -o ControlMaster=auto -o ControlPersist=15m'"
    ]
    extra_arguments = [
      "--extra-vars",
      "ansible_host=${var.target_repo} ansible_connection=${var.ansible_connection}"
    ]
    groups = [
      "all",
      "private",
      "users",
      "image",
      "${var.image_name}"
    ]
    playbook_file = "../ansible/${var.ansible_playbook}"
    user = "root"
  }

  post-processor "docker-tag" {
    repository = "${var.local_user}/${var.target_repo}"
    tags = ["${var.target_tag}"]
  }
}
