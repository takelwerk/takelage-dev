[![license](https://img.shields.io/github/license/takelwerk/takelage-dev?color=blueviolet)](https://github.com/takelwerk/takelage-dev/blob/main/LICENSE)
[![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelage/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelwerk/takelage)
[![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_deploy_project_on_push.yml)
[![deploy takelbeta](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Build,%20test%20and%20deploy%20takelbeta?label=deploy%20takelbeta)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_deploy_takelbeta_on_push.yml)
[![deploy takelbuild](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Build,%20test%20and%20deploy%20takelbuild?label=deploy%20takelbuild)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_deploy_takelbuild_on_push.yml)
[![test project](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Build%20and%20test%20project?label=test%20project)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_project_nightly.yml)
[![test roles](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Test%20roles?label=test%20roles)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_roles_nightly.yml)

# takelage-dev

*takelage-dev* is the development environment 
of the takelage devops workflow.
The takelage devops workflow helps devops engineers
build, test and deploy os images.

*takelage-dev* is a
[Docker](https://www.docker.com) image 
[takelwerk/takelage](http://hub.docker.com/r/takelwerk/takelage)
which based on the official [Debian](https://www.debian.org) docker image
[bullseye-slim](https://hub.docker.com/_/debian). 
It builds itself.

## Framework Versions

| App | Artifact |
| --- | -------- |
| *[takelage-doc](https://github.com/takelwerk/takelage-doc)* | [![License](https://img.shields.io/github/license/takelwerk/takelage-doc?color=blueviolet)](https://github.com/takelwerk/takelage-doc/blob/main/LICENSE) |
| *[takelage-dev](https://github.com/takelwerk/takelage-dev)* | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelage/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelwerk/takelage) |
| *[takelage-pad](https://github.com/takelwerk/takelage-pad)* | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelpad/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelwerk/takelpad) |
| *[takelage-cli](https://github.com/takelwerk/takelage-cli)* | [![rubygems.org](https://img.shields.io/gem/v/takeltau?label=rubygems.org&color=blue)](https://rubygems.org/gems/takeltau) |
| *[takelage-var](https://github.com/takelwerk/takelage-var)* | [![pypi,org](https://img.shields.io/pypi/v/pytest-takeltest?label=pypi.org&color=blue)](https://pypi.org/project/pytest-takeltest/) |
| *[takelage-img-takelslim](https://github.com/takelwerk/takelage-img-takelslim)* | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelslim/latest?label=hub.docker.com&color=blue)](https://hub.docker.com/r/takelwerk/takelslim) | 
| *[takelage-img-takelbase](https://github.com/takelwerk/takelage-img-takelbase)* | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelbase/latest?label=hub.docker.com&color=blue)](https://hub.docker.com/r/takelwerk/takelbase) | 
| *[takelage-img-takelruby](https://github.com/takelwerk/takelage-img-takelruby)* | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelruby/latest?label=hub.docker.com&color=blue)](https://hub.docker.com/r/takelwerk/takelruby) | 
| *[takelage-vbox-takelbase](https://github.com/takelwerk/takelage-vbox-takelbase)* | [![vagrantup.com](https://img.shields.io/badge/vagrantup.com-debian--bullseye-blue)](https://app.vagrantup.com/takelwerk/boxes/takelbase) | 

## Framework Status

| App | Deploy project | Test project | Test roles | Deploy vbox |
| --- | -------------- | ------------ | ---------- | ----------- |
| *[takelage-dev](https://github.com/takelwerk/takelage-dev)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Build%20and%20test%20project?label=test%20project)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_project_nightly.yml) | [![test roles](https://img.shields.io/github/workflow/status/takelwerk/takelage-dev/Test%20roles?label=test%20roles)](https://github.com/takelwerk/takelage-dev/actions/workflows/build_test_roles_nightly.yml) |
| *[takelage-pad](https://github.com/takelwerk/takelage-pad)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-pad/Build,%20test%20and%20deploy%20project%20to%20dockerhub?label=deploy%20project)](https://github.com/takelwerk/takelage-pad/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/takelwerk/takelage-pad/Build%20and%20test%20project?label=test%20project)](https://github.com/takelwerk/takelage-pad/actions/workflows/build_test_project_nightly.yml) | [![test roles](https://img.shields.io/github/workflow/status/takelwerk/takelage-pad/Build%20and%20test%20roles?label=test%20roles)](https://github.com/takelwerk/takelage-pad/actions/workflows/build_test_roles_nightly.yml) | [![deploy vbox](https://img.shields.io/github/workflow/status/takelwerk/takelage-pad/Build%20and%20deploy%20project%20vbox%20to%20vagrantup?label=deploy%20vbox)](https://github.com/takelwerk/takelage-pad/actions/workflows/build_deploy_project_vbox_on_push.yml) |
| *[takelage-cli](https://github.com/takelwerk/takelage-cli)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-cli/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/takelwerk/takelage-cli/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/takelwerk/takelage-cli/Test%20project?label=test%20project)](https://github.com/takelwerk/takelage-cli/actions/workflows/test_project_nightly.yml) |
| *[takelage-var](https://github.com/takelwerk/takelage-var)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-var/Build,%20test%20and%20deploy%20project?label=deploy%20project)](https://github.com/takelwerk/takelage-var/actions/workflows/build_test_deploy_project_on_push.yml) | [![test project](https://img.shields.io/github/workflow/status/takelwerk/takelage-var/Build%20and%20test%20project?label=test%20project)](https://github.com/takelwerk/takelage-var/actions/workflows/build_test_project_nightly.yml) |
| *[takelage-img-takelslim](https://github.com/takelwerk/takelage-img-takelslim)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-img-takelslim/Build%20and%20deploy%20takelslim?label=deploy%20project)](https://github.com/takelwerk/takelage-img-takelslim/actions/workflows/build_deploy_takelslim_nightly.yml) |
| *[takelage-img-takelbase](https://github.com/takelwerk/takelage-img-takelbase)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-img-takelbase/Build%20and%20deploy%20takelbase?label=deploy%20project)](https://github.com/takelwerk/takelage-img-takelbase/actions/workflows/build_deploy_takelbase_nightly.yml) |
| *[takelage-img-takelruby](https://github.com/takelwerk/takelage-img-takelruby)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-img-takelruby/Build%20and%20deploy%20takelruby%20latest?label=deploy%20project)](https://github.com/takelwerk/takelage-img-takelruby/actions/workflows/build_deploy_takelruby_nightly.yml) |
| *[takelage-vbox-takelbase](https://github.com/takelwerk/takelage-vbox-takelbase)* | [![deploy project](https://img.shields.io/github/workflow/status/takelwerk/takelage-vbox-takelbase/Build%20and%20deploy%20project?label=deploy%20project)](https://github.com/takelwerk/takelage-vbox-takelbase/actions/workflows/build_and_deploy_project_nightly.yml) | | | [![deploy vbox](https://img.shields.io/github/workflow/status/takelwerk/takelage-vbox-takelbase/Build%20and%20deploy%20project?label=deploy%20vbox)](https://github.com/takelwerk/takelage-vbox-takelbase/actions/workflows/build_and_deploy_project_nightly.yml) |

## takelage-dev Overview

This project is an example of the takelage devops workflow as
it builds a docker image called 
[takelwerk/takelage](https://hub.docker.com/r/takelwerk/takelage).
This docker image is the development environment you can use
to create your own projects based on the takelage devops workflow.

Every time you start the takelage environment in a new directory
a new container will be started.
When you start the takelage environment for a second time in a
directory you will log in to the already running container.
So you have one container for each project,
but you can have many shells per project.

takelage has been tested under macOS Monterey and Debian Bullseye hosts.

## Channels

takelage comes in different flavors.
* `takelwerk/takelage` is the interactive environment 
* `takelwerk/takelbeta` is the development version of `takelwerk/takelage`
* `takelwerk/takelbuild` is a smaller version for CI/CD pipelines

`takelwerk/takelage` is based on
[takelage-img-takelslim](https://github.com/takelwerk/takelage-img-takelslim)
which is basically a 
[debian:bullseye-slim](https://hub.docker.com/_/debian)
docker 
[official image](https://docs.docker.com/docker-hub/official_images/)
with a
[minimal python3](https://github.com/takelwerk/takelage-img-takelslim/blob/main/packer/templates/takelslim/build.pkr.hcl)
installed for 
[ansible](https://docs.ansible.com/ansible/latest/).

There is also a systemd based base container
[takelage-img-takelbase](https://github.com/takelwerk/takelage-img-takelbase)
which has 
[python3, sudo and systemd](https://github.com/takelwerk/takelage-img-takelbase/blob/main/packer/templates/takelbase/bin/install-debian.bash)
installed and mimics an old-fashioned debian box. 
It is designed to be run with the docker
`--privileged` flag with extended privileges.
