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

## Takelage DevOps Workflow

This project is an example of the takelage devops workflow as
it builds a docker image called 
[takelage](https://hub.docker.com/r/takelage/takelage).
This docker image is the development environment you cand use
to create your own projects based on the takelage devops workflow.
