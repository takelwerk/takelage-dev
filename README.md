[![license](https://img.shields.io/github/license/geospin-takelage/takelage-dev?color=blueviolet)](https://github.com/geospin-takelage/takelage-dev/blob/main/LICENSE)
[![hub.docker.com](https://img.shields.io/docker/v/takelage/takelage/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelage/takelage)
[![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-dev/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_deploy_project_on_push.yml)
[![test project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-dev/Build%20and%20test%20project?label=test%20project)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_project_nightly.yml)
[![test roles](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-dev/Test%20roles?label=test%20roles)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_roles_nightly.yml)

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

## Framework Versions

| App | Artifact |
| --- | -------- |
| *[takelage-doc](https://github.com/geospin-takelage/takelage-doc)* | [![License](https://img.shields.io/github/license/geospin-takelage/takelage-doc?color=blueviolet)](https://github.com/geospin-takelage/takelage-doc/blob/main/LICENSE) |
| *[takelage-dev](https://github.com/geospin-takelage/takelage-dev)* | [![hub.docker.com](https://img.shields.io/docker/v/takelage/takelage/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelage/takelage) |
| *[takelage-cli](https://github.com/geospin-takelage/takelage-cli)* | [![rubygems.org](https://img.shields.io/gem/v/takelage?label=rubygems.org&color=blue)](https://rubygems.org/gems/takelage) |
| *[takelage-var](https://github.com/geospin-takelage/takelage-var)* | [![pypi,org](https://img.shields.io/pypi/v/takeltest?label=pypi.org&color=blue)](https://pypi.org/project/takeltest/) |
| *[takelage-bit](https://github.com/geospin-takelage/takelage-bit)* | [![hub.docker.com](https://img.shields.io/docker/v/takelage/bitboard/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelage/bitboard) | 
| *[takelage-img-takelslim](https://github.com/geospin-takelage/takelage-img-takelslim)* | [![hub.docker.com](https://img.shields.io/docker/v/takelage/takelslim/latest?label=hub.docker.com&color=blue)](https://hub.docker.com/r/takelage/takelslim) | 
| *[takelage-img-takelbase](https://github.com/geospin-takelage/takelage-img-takelbase)* | [![hub.docker.com](https://img.shields.io/docker/v/takelage/takelbase/latest?label=hub.docker.com&color=blue)](https://hub.docker.com/r/takelage/takelbase) | 

## Framework Status

| App | Deploy project | Test project | Test roles |
| --- | -------------- | ------------ | ---------- |
| *[takelage-dev](https://github.com/geospin-takelage/takelage-dev)* | [![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-dev/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-dev/Build%20and%20test%20project?label=test%20project)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_project_nightly.yml) | [![test roles](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-dev/Test%20roles?label=test%20roles)](https://github.com/geospin-takelage/takelage-dev/actions/workflows/build_test_roles_nightly.yml) |
| *[takelage-cli](https://github.com/geospin-takelage/takelage-cli)* | [![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-cli/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/geospin-takelage/takelage-cli/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-cli/Test%20project?label=test%20project)](https://github.com/geospin-takelage/takelage-cli/actions/workflows/test_project_nightly.yml) |
| *[takelage-var](https://github.com/geospin-takelage/takelage-var)* | [![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-var/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/geospin-takelage/takelage-var/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-var/Build%20and%20test%20project?label=test%20project)](https://github.com/geospin-takelage/takelage-var/actions/workflows/build_test_project_nightly.yml) |
| *[takelage-bit](https://github.com/geospin-takelage/takelage-bit)* | [![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-bit/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/geospin-takelage/takelage-bit/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-bit/Build%20and%20test%20project?label=test%20project)](https://github.com/geospin-takelage/takelage-bit/actions/workflows/build_test_project_nightly.yml) | [![test roles](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-bit/Test%20roles?label=test%20roles)](https://github.com/geospin-takelage/takelage-bit/actions/workflows/build_test_roles_nightly.yml) |
| *[takelage-img-takelslim](https://github.com/geospin-takelage/takelage-img-takelslim)* | [![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-img-takelslim/Build%20and%20deploy%20takelslim?label=deploy%20project)](https://github.com/geospin-takelage/takelage-img-takelslim/actions/workflows/build_deploy_takelslim_nightly.yml) |
| *[takelage-img-takelbase](https://github.com/geospin-takelage/takelage-img-takelbase)* | [![deploy project](https://img.shields.io/github/workflow/status/geospin-takelage/takelage-img-takelbase/Build%20and%20deploy%20takelbase?label=deploy%20project)](https://github.com/geospin-takelage/takelage-img-takelbase/actions/workflows/build_deploy_takelbase_nightly.yml) |

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
[python3-minimal](https://packages.debian.org/buster/python3-minimal) and
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
with a
[minimal python3](https://github.com/geospin-takelage/takelage-img-takelslim/blob/main/packer/templates/docker/takelslim/debian-buster/packer.json)
installed for 
[ansible](https://docs.ansible.com/ansible/latest/).

Up to version 0.30 takelage was based on
[takelage-img-takelbase](https://github.com/geospin-takelage/takelage-img-takelbase)
which has 
[python3, sudo and systemd](https://github.com/geospin-takelage/takelage-img-takelbase/blob/main/packer/templates/docker/takelbase/debian-buster/bin/install-debian.bash)
installed. These takelage containers were run with the
`--privileged` flag with extended privileges.
This method was developed to simulate an old-fashioned
debian systemd server but it is generally not needed for takelage-dev.

Accordingly, the takelage command line tool `tau` from the 
[ruby gem takelage](https://github.com/geospin-takelage/takelage-cli)
beginning with version 0.27 which is part of takelage 0.31
dropped the `--privileged` flag. 

For
[takelage-cli](https://github.com/geospin-takelage/takelage-cli)
for example the `--privileged` flag is still needed.
So if you want to run privileged takelage containers you can 
[overwrite the setting](https://github.com/geospin-takelage/takelage-cli#configuration)
by adding `docker_run_options: --privileged` 
to a 
[project `takelage.yml`](https://github.com/geospin-takelage/takelage-cli/blob/main/.github/workflows/test_project_nightly.yml)
or your `~/.takelage.yml`.

Afterwards, you can check your active config with `tau config`.
If you still run into problems, try the helpful
 `tau -l debug` flag or drop us a line.
