[![takelage image](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_project_nightly.yml/badge.svg)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_project_nightly.yml)
[![ansible roles](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_roles_nightly.yml/badge.svg)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_roles_nightly.yml)
[![docker image](https://img.shields.io/docker/v/takelage/takelage/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelage/takelage)
[![license](https://img.shields.io/github/license/geospin-takelage/takelage-dev?label=License&color=blueviolet)](https://github.com/geospin-takelage/takelage-dev/blob/main/LICENSE)


# takelage-dev

*takelage-dev* is the development environment 
of the takelage devops workflow.
The takelage devops workflow helps devops engineers
build, test and deploy os images.

*takelage-dev* is a
[Docker](https://www.docker.com) image 
[takelage/takelage](http://hub.docker.com/r/takelage/takelage)
which based on the official [Debian](https://www.debian.org) docker image
[buster-slim](https://hub.docker.com/_/debian). 
It builds itself.

## Framework

The takelage devops framework consists of these projects:

| App | Description |
| --- | ----------- |
| *[takelage-doc](https://github.com/geospin-takelage/takelage-doc)* | takelage documentation |
| *[takelage-dev](https://github.com/geospin-takelage/takelage-dev)* | takelage development environment |
| *[takelage-var](https://github.com/geospin-takelage/takelage-var)* | takelage test plugin |
| *[takelage-cli](https://github.com/geospin-takelage/takelage-cli)* | takelage command line interface |
| *[takelage-bit](https://github.com/geospin-takelage/takelage-bit)* | takelage bit server | 
| *[takelage-img-takelbase](https://github.com/geospin-takelage/takelage-img-takelbase)* | takelage takelbase image | 
| *[takelage-img-takelslim](https://github.com/geospin-takelage/takelage-img-takelslim)* | takelage takelbase image | 
| *[takelage-img-multipostgres](https://github.com/geospin-takelage/takelage-img-multipostgres)* | takelage multipostgres image | 

## takelage-dev Overview

This project is an example of the takelage devops workflow as
it builds a docker image called 
[takelage](https://hub.docker.com/r/takelage/takelage).
This docker image is the development environment you can use
to create your own projects based on the takelage devops workflow.

Every time you start the takelage environment in a new directory
a new container will be started.
When you start the takelage environment for a second time in a
directory you will log in to the already running container.
So you have one container for each project,
but you can have many shells per project.

takelage has been tested under macOS Catalina and Debian Buster hosts.
The [takelage](https://hub.docker.com/r/takelage/takelage)
docker image is based on the Debian 
[buster-slim](https://hub.docker.com/_/debian)
docker image.
The Debian base image is used by 
[packer](https://packer.io)
to create the
[takelslim](https://hub.docker.com/r/takelage/takelslim)
docker image by installing 
[python3](https://packages.debian.org/buster/python3) and
[python3-apt](https://packages.debian.org/buster/python3-apt).
The takelslim docker image is then used to create
the takelage docker image.

## Versions

Since version 0.31 takelage is based on
[takelage-img-takelslim](https://github.com/geospin-takelage/takelage-img-takelslim)
which is basically a 
[debian:buster-slim](https://hub.docker.com/_/debian)
docker 
[official image](https://docs.docker.com/docker-hub/official_images/)
with 
[python3-minimal](https://github.com/geospin-takelage/takelage-img-takelslim/blob/main/packer/templates/docker/takelslim/debian-buster/packer.json)
to run 
[ansible](https://docs.ansible.com/ansible/latest/).

Up to version 0.30 takelage was based on
[takelage-img-takelbase](https://github.com/geospin-takelage/takelage-img-takelbase)
which has 
[python3, sudo and systemd](https://github.com/geospin-takelage/takelage-img-takelbase/blob/main/packer/templates/docker/takelbase/debian-buster/bin/install-debian.bash)
installed. These takelage containers were run with the
`--privileged` flag with extended privileges.
This method was developed to simulate an old-fashioned
debian systemd server it is not needed for takelage-dev.

Accordingly the takelage command line tool `tau` from the 
[ruby gem takelage](https://github.com/geospin-takelage/takelage-cli)
dropped the `--privileged` flag 
starting from version 0.27 which is part of takelage 0.31. 

The docker run command is stored in the `cmd_docker_container_create` setting 
which can be inspected with `tau self config default`. 
If you want to run containers with the `--privileged` flag you can 
[overwrite the setting](https://github.com/geospin-takelage/takelage-cli#configuration)
in  a project `takelage.yml` or in your `~/.takelage.yml` and add the flag.
Afterwards, check your final config with `tau self config active`.
