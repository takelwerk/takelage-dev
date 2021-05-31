source "docker" "takelage" {
  export_path = "images/docker/${var.target_repo}-${var.target_tag}.tar"
  image = "${var.base_user}/${var.base_repo}:${var.base_tag}"
  pull = false
  run_command = "${local.run_command}"
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
      "${var.ansible_environment}"
    ]
    playbook_file = "../ansible/${var.ansible_playbook}"
    user = "root"
  }

  post-processor "docker-import" {
    changes = [
      "CMD [\"${var.command}\"]",
      "ENV DEBIAN_FRONTEND=noninteractive",
      "ENV LANG=en_US.UTF-8",
      "ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "WORKDIR /root"
    ]
    repository = "${var.local_user}/${var.target_repo}"
    tag = "${var.target_tag}"
  }
}
