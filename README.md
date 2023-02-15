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

| Project                                                                                                                                                             | Artifacts                                                                                                                                                                                                                                                                                                                                                                 |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [![takelage-doc](https://img.shields.io/badge/github-takelage--doc-purple)](https://github.com/takelwerk/takelage-doc)                                            | [![License](https://img.shields.io/badge/license-GNU_GPLv3-blue)](https://github.com/takelwerk/takelage-doc/blob/main/LICENSE)                                                                                                                                                                                                                                            |
| [![takelage-img-takelslim](https://img.shields.io/badge/github-takelage--img--takelslim-purple)](https://github.com/takelwerk/takelage-img-takelslim)             | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelslim/latest?label=hub.docker.com&arch=amd64&color=teal)](https://hub.docker.com/r/takelwerk/takelslim) [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelslim/latest?label=hub.docker.com&arch=arm64&color=slateblue)](https://hub.docker.com/r/takelwerk/takelslim)                  | 
| [![takelage-img-takelbase](https://img.shields.io/badge/github-takelage--img--takelbase-purple)](https://github.com/takelwerk/takelage-img-takelbase)             | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelbase/latest?label=hub.docker.com&arch=amd64&color=teal)](https://hub.docker.com/r/takelwerk/takelbase) [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelbase/latest?label=hub.docker.com&arch=arm64&color=slateblue)](https://hub.docker.com/r/takelwerk/takelbase)                    | 
| [![takelage-img-takelruby](https://img.shields.io/badge/github-takelage--img--takelruby-purple)](https://github.com/takelwerk/takelage-img-takelruby)             | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelruby/latest?label=hub.docker.com&arch=amd64&color=teal)](https://hub.docker.com/r/takelwerk/takelruby) [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelruby/latest?label=hub.docker.com&arch=arm64&color=slateblue)](https://hub.docker.com/r/takelwerk/takelruby)                    | 
| [![takelage-vagrant-takelbase](https://img.shields.io/badge/github-takelage--vagrant--takelbase-purple)](https://github.com/takelwerk/takelage-vagrant-takelbase) | [![vagrantup.com](https://img.shields.io/badge/vagrantup.com-debian--bullseye-blue)](https://app.vagrantup.com/takelwerk/boxes/takelbase)                                                                                                                                                                                                                                 | 
| [![takelage-var](https://img.shields.io/badge/github-takelage--var-purple)](https://github.com/takelwerk/takelage-var)                                            | [![pypi,org](https://img.shields.io/pypi/v/pytest-takeltest?label=pypi.org&color=blue)](https://pypi.org/project/pytest-takeltest/)                                                                                                                                                                                                                                       |
| [![takelage-cli](https://img.shields.io/badge/github-takelage--cli-purple)](https://github.com/takelwerk/takelage-cli)                                            | [![rubygems.org](https://img.shields.io/gem/v/takeltau?label=rubygems.org&color=blue)](https://rubygems.org/gems/takeltau)                                                                                                                                                                                                                                                |
| [![takelage-dev](https://img.shields.io/badge/github-takelage--dev-purple)](https://github.com/takelwerk/takelage-dev)                                            | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelage/latest?label=hub.docker.com&arch=amd64&sort=semver&color=teal)](https://hub.docker.com/r/takelwerk/takelage) [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelage/latest?label=hub.docker.com&arch=arm64&sort=semver&color=slateblue)](https://hub.docker.com/r/takelwerk/takelage) |
| [![takelage-pad](https://img.shields.io/badge/github-takelage--pad-purple)](https://github.com/takelwerk/takelage-pad)                                            | [![hub.docker.com](https://img.shields.io/docker/v/takelwerk/takelpad/latest?label=hub.docker.com&sort=semver&color=blue)](https://hub.docker.com/r/takelwerk/takelpad)                                                                                                                                                                                                   |

## Framework Status

| Project                                                                                                                                                 | Pipelines                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [![takelage-img-takelslim](https://img.shields.io/badge/github-takelage--img--takelslim-purple)](https://github.com/takelwerk/takelage-img-takelslim) | [![takelslim amd64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-img-takelslim/takelslim_amd64.yml?label=takelslim%20amd64)](https://github.com/takelwerk/takelage-img-takelslim/actions/workflows/takelslim_amd64.yml) [![takelslim arm64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-img-takelslim/takelslim_arm64.yml?label=takelslim%20arm64)](https://github.com/takelwerk/takelage-img-takelslim/actions/workflows/takelslim_arm64.yml) |
| [![takelage-img-takelbase](https://img.shields.io/badge/github-takelage--img--takelbase-purple)](https://github.com/takelwerk/takelage-img-takelbase) | [![takelbase amd64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-img-takelbase/takelbase_amd64.yml?label=takelbase%20amd64)](https://github.com/takelwerk/takelage-img-takelbase/actions/workflows/takelbase_amd64.yml) [![takelbase arm64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-img-takelbase/takelbase_arm64.yml?label=takelbase%20arm64)](https://github.com/takelwerk/takelage-img-takelbase/actions/workflows/takelbase_arm64.yml) |
| [![takelage-img-takelruby](https://img.shields.io/badge/github-takelage--img--takelruby-purple)](https://github.com/takelwerk/takelage-img-takelruby) | [![takelruby amd64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-img-takelruby/takelruby_amd64.yml?label=takelruby%20amd64)](https://github.com/takelwerk/takelage-img-takelruby/actions/workflows/takelruby_amd64.yml) [![takelruby arm64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-img-takelruby/takelruby_arm64.yml?label=takelruby%20arm64)](https://github.com/takelwerk/takelage-img-takelruby/actions/workflows/takelruby_arm64.yml) |
| [![takelage-vagrant-takelbase](https://img.shields.io/badge/github-takelage--vagrant--takelbase-purple)](https://github.com/takelwerk/takelage-vagrant-takelbase) | [![virtualbox](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-vagrant-takelbase/virtualbox.yml?label=virtualbox)](https://github.com/takelwerk/takelage-vagrant-takelbase/actions/workflows/virtualbox.yml)                                                                                                                                                                                                                                                                   |
| [![takelage-var](https://img.shields.io/badge/github-takelage--var-purple)](https://github.com/takelwerk/takelage-var) | [![takeltest](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-var/takeltest.yml?label=takeltest)](https://github.com/takelwerk/takelage-var/actions/workflows/takeltest.yml) [![test_takeltest](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-var/test_takeltest.yml?label=test%20takeltest)](https://github.com/takelwerk/takelage-var/actions/workflows/test_takeltest.yml)                                                                       |
| [![takelage-cli](https://img.shields.io/badge/github-takelage--cli-purple)](https://github.com/takelwerk/takelage-cli) | [![takeltau](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-cli/takeltau.yml?label=takeltau)](https://github.com/takelwerk/takelage-cli/actions/workflows/takeltau.yml) [![test_takeltau](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-cli/test_takeltau.yml?label=test%20takeltau)](https://github.com/takelwerk/takelage-cli/actions/workflows/test_takeltau.yml)                                                                               |
| [![takelage-dev](https://img.shields.io/badge/github-takelage--dev-purple)](https://github.com/takelwerk/takelage-dev) | [![takelage amd64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/takelage_amd64.yml?label=takelage%20amd64)](https://github.com/takelwerk/takelage-dev/actions/workflows/takelage_amd64.yml) [![takelage arm64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/takelage_arm64.yml?label=takelage%20arm64)](https://github.com/takelwerk/takelage-dev/actions/workflows/takelage_arm64.yml)                                                 |
| | [![takelbeta amd64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/takelbeta_amd64.yml?label=takelbeta%20amd64)](https://github.com/takelwerk/takelage-dev/actions/workflows/takelbeta_amd64.yml) [![takelbeta arm64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/takelbeta_arm64.yml?label=takelbeta%20arm64)](https://github.com/takelwerk/takelage-dev/actions/workflows/takelbeta_arm64.yml)                                         |
| | [![takelbuild amd64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/takelbuild_amd64.yml?label=takelbuild%20amd64)](https://github.com/takelwerk/takelage-dev/actions/workflows/takelbuild_amd64.yml) [![takelbuild arm64](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/takelbuild_arm64.yml?label=takelbuild%20arm64)](https://github.com/takelwerk/takelage-dev/actions/workflows/takelbuild_arm64.yml)                                 |
| | [![test_takelage](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/test_takelage.yml?label=test%20takelage)](https://github.com/takelwerk/takelage-dev/actions/workflows/test_takelage.yml) [![test_roles](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/test_roles.yml?label=test%20roles)](https://github.com/takelwerk/takelage-dev/actions/workflows/test_roles.yml)                                                                     |
| | [![test_takelbuild](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-dev/test_takelbuild.yml?label=test%20takelbuild)](https://github.com/takelwerk/takelage-dev/actions/workflows/test_takelbuild.yml)                                                                                                                                                                                                                                                                         |
| [![takelage-pad](https://img.shields.io/badge/github-takelage--pad-purple)](https://github.com/takelwerk/takelage-pad) | [![takelpad_docker](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-pad/takelpad_docker.yml?label=takelpad_docker)](https://github.com/takelwerk/takelage-pad/actions/workflows/takelpad_docker.yml) [![takelpad_virtualbox](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-pad/takelpad_virtualbox.yml?label=takelpad_virtualbox)](https://github.com/takelwerk/takelage-pad/actions/workflows/takelpad_virtualbox.yml)                             |
| | [![test_takelpad](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-pad/test_takelpad.yml?label=test_takelpad)](https://github.com/takelwerk/takelage-pad/actions/workflows/test_takelpad.yml) [![test_roles](https://img.shields.io/github/actions/workflow/status/takelwerk/takelage-pad/test_roles.yml?label=test_roles)](https://github.com/takelwerk/takelage-pad/actions/workflows/test_roles.yml)                                                                         |

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
[minimal python3](https://github.com/takelwerk/takelage-img-takelslim/blob/main/packer/templates/takelslim/docker/main.pkr.hcl)
installed for 
[ansible](https://docs.ansible.com/ansible/latest/).

There is also a systemd based base container
[takelage-img-takelbase](https://github.com/takelwerk/takelage-img-takelbase)
which has 
[python3, sudo and systemd](https://github.com/takelwerk/takelage-img-takelbase/blob/main/packer/templates/takelbase/docker/bin/install-debian.bash)
installed and mimics an old-fashioned debian box. 
It is designed to be run with the docker
`--privileged` flag with extended privileges.
