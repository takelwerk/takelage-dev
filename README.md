# takelage-dev

*takelage-dev* is the development environment 
of the takelage devops workflow.
The takelage devops workflow helps devops engineers
build, test and deploy os images.

The *takelage-dev* 
[Docker](https://www.docker.com) image is based
on the official [Debian](https://www.debian.org) docker image
[buster-slim](https://hub.docker.com/_/debian).

## Framework

The takelage devops framework consists of these projects:

| App | Description |
| --- | ----------- |
| *[takelage-dev](https://github.com/geospin-takelage/takelage-dev)* | takelage development environment |
| *[takelage-var](https://github.com/geospin-takelage/takelage-var)* | takelage test plugin |
| *[takelage-cli](https://github.com/geospin-takelage/takelage-cli)* | takelage command line interface |
| *[takelage-bit](https://github.com/geospin-takelage/takelage-bit)* | takelage bit server | 

## Takelage DevOps Workflow

The takelage devops workflow uses
[packer](https://packer.io/docs/builders/index.html), 
[ansible](https://docs.ansible.com/) and 
[molecule](https://molecule.readthedocs.io/)
to test-driven create machine images from code.
Although the target platforms are only limited 
by the packer builders the main target platform
of takelage are 
[docker containers](https://www.docker.com/resources/what-container).

Docker Containers can replace traditional VMs in the Cloud on 
[Google Compute Engine](https://cloud.google.com/compute/docs/containers),
using the
[Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
or running as
[Azure Container Instances](https://azure.microsoft.com/en-us/services/container-instances/).
But the most important virtualization technology is
Google's [Kubernetes](https://kubernetes.io/) which has  
gained wide-spread adoption in the DevOps community
and can be considered as the default virtualization
environment to run docker containers.

Docker containers are spawned from docker images and the
most common way to build docker images are
[Dockerfiles](https://docs.docker.com/engine/reference/builder/).
Dockerfiles are written in a domain-specific language that uses 
standard bash commands as its core. 
As one-container-one-process is a recommended design pattern
for dockerized applications it makes sense to create really simple 
Dockerfiles. So what‘s wrong with Dockerfiles?

Here are some answers:

- Dockerfiles cannot be tested easily. Bash has never been good at that.
- Dockerfiles produce large images. Those that do not are full of logical AND
  operators which makes testing even more cumbersome.
- Dockerfiles are not reusable. The use of Dockerfiles promotes copy and paste
  which violates the 
  [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself)
  principle.
- Dockerfiles can only produce docker images target no other platform. 

This is why we propose a new workflow to build docker images:

- Build the images with packer.
- Write the provisioning code in ansible.
- Use ansible roles to reuse code and share them with 
  [bit](https://bit.dev) between 
  [git](https://git-scm.com) repositories.
- Use a molecule development environment.
- Test the code with 
  [pytest](https://docs.pytest.org/en/latest/), 
  [testinfra](https://testinfra.readthedocs.io/en/latest/) and 
  [takeltest](https://github.com/geospin-takelage/takelage-var).

This project is an example of the takelage devops workflow.
It produces a docker image called 
[takelage](https://hub.docker.com/r/takelage/takelage).
This image is the development environment you use to create
your own projects based on the takelage devops workflow.

## Nomenclature

[Takelage](https://de.wikipedia.org/wiki/Takelage) is the German word for
[rigging](https://en.wikipedia.org/wiki/Rigging).  
It “comprises the system of ropes, cables and chains, 
which support a sailing ship’s masts 
and which adjust the position of the vessel’s 
sails and spars to which they are attached”. 
It symbolizes the software wiring 
which configures the docker containers – 
another word from the nautical world.
It is 
[pronounced](https://cdn.duden.de/_media_/audio/ID4112295_148090832.mp3)
with a French ending.

[Takel](https://de.wikipedia.org/wiki/Talje) is the German word for 
[tackle](https://en.wikipedia.org/wiki/Block_and_tackle).

[Tau](https://de.wikipedia.org/wiki/Tauwerk) is the German word for 
[rope](https://en.wikipedia.org/wiki/Rope). 
It is pronounced the same way as the Greek letter [τ](https://en.wikipedia.org/wiki/Tau).
