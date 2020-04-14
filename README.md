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

## Takelage Overview

This project is an example of the takelage devops workflow as
it builds a docker image called 
[takelage](https://hub.docker.com/r/takelage/takelage).
This docker image is the development environment you cand use
to create your own projects based on the takelage devops workflow.

Every time you start the takelage environment in a new directory
a new container will be started.
When you start the takelage environment for a second time in a
directory you will log in to the already running container.
So you have one container for each project,
but you can have many shells per project.

takelage has been tested under macOS Catalina and Debian Buster hosts.
The [takelage](https://hub.docker.com/r/takelage/takelage).
docker image is based on the Debian 
[buster-slim](https://hub.docker.com/_/debian)
docker image.
The Debian base image is used by 
[packer](https://packer.io)
to create the
[takelbase](https://hub.docker.com/r/takelage/takelbase)
docker image by installing 
[python3](https://packages.debian.org/buster/python3),
[python3-apt](https://packages.debian.org/buster/python3-apt)
and [systemd](https://packages.debian.org/buster/systemd).
The takelbase docker image is then used to create
the takelage docker image.

## Getting Started

### Prerequisites

On your host system install these prerequisites:
- [docker](https://docs.docker.com/get-docker/)
If you use linux be sure to follow the 
[postinstall](https://docs.docker.com/engine/install/linux-postinstall/) 
guide
- [socat](http://www.dest-unreach.org/socat/)
- [gnupg](https://gnupg.org/)
- [git](https://git-scm.com)
- [gopass](https://www.gopass.pw)

### Command Line Interfaces

For the global takelage `tau` command line interface you'll need `ruby`. 
You may use your system ruby but it is recommended to install it as user:
- [ruby via rvm](https://rvm.io): First install gpg keys then:
```bash
\curl -sSL https://get.rvm.io | bash -s stable --ruby
```
- [tau via gem](https://github.com/geospin-takelage/takelage-cli) (as user): 
```bash
gem install takelage
```
- You can add `tau` autocompletion to your bash startup script:
```bash
source <(tau completion bash)
```
- Use `tau` to get the latest 
[takelage docker image](https://hub.docker.com/r/takelage/takelage) 
from hub.docker.com: 
```bash
tau update
```
- Every project has its own local command line interface using the
[rake](https://github.com/ruby/rake) build utility.
The available commands can be inspected by running
```bash
rake
```

### Configuration

takelage uses the GnuPG SSH agent. You need:

- `AddKeysToAgent yes` in your `~/.ssh/config`
- `enable-ssh-support` in your `~/.gnupg/gpg-agent.conf`
- `gpgconf --launch gpg-agent` in your `.bash_profile`/`.bashrc`
- `export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)` 
in your `.bash_profile`/`.bashrc`

Please make sure that the following lines are **NOT** part
of your configuration:

- `UseKeychain yes` **NOT** in your `~/.ssh/config`

You may need to reboot your system so that the changes take effect.

You should init gopass:

```bash
gopass init
```

Then list the key id of you gpg key:

```bash
gpg --list-keys
```

Add the key id of your gpg key as your git signing key
and add your name and e-mail address to your git config:

```bash
git config --global user.signingkey <key-id>
git config --global user.name "my name"
git congig --global user.email "myname@example.com"
```

Go into your project directory and run
```bash
tau login
```

Remember that you can always run `tau` with `-l debug`
to see what's going on. Have fun!
