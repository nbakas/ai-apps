# Introduction

This walkthrough explains the Dockerfile and the reasoning behind each step. It is intended for developers who want to understand how to build a hardened Docker image for Python applications, LLMs, inference, run streamlit apps, compile LaTeX documents, make static images with Kaleido, etc. It can be run locally as well as on Hugging Face Spaces. It is based on the NVIDIA CUDA runtime base image for GPU support, but can be adapted to CPU-only systems.

## Docker Images

A Docker image is an immutable, read-only template used to create containers. It contains the application, runtime, libraries, packages, and configuration. You cannot edit an existing image directly; use a Dockerfile to build a new image with additional layers. Images contain read-only filesystem layers. 

- https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/
- https://docs.docker.com/get-started/docker-concepts/building-images/
- `docker images` → lists all local images.

## Docker Containers

A Docker container is a running or stopped instance of an image. It adds a writable layer where you can install packages or modify files, but these changes do not modify the original image and disappear when the container is removed. Containers add a writable filesystem layer.

- https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/
- https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/
- `docker ps -a` → lists all containers, including stopped ones.

## Context

We will be using Interactive container to understand the steps from a base image and on, and finally we will build an image for development and production with a `Dockerfile`.

- Interactive container: no new image layers. Your changes go into the container's writable layer.
- Dockerfile build: new image layers are created on top of the NVIDIA base.
- Run commands from any shell where the Docker Command-Line Interface (CLI) is available.
- Docker must be running.


## Terminology

- `WSL 2` = Windows Subsystem for Linux version 2. It uses lightweight virtualization to run Linux environments on Windows.
- `Hyper-V` = Windows virtualization technology used to create isolated virtual machines (VMs). WSL 2 uses Microsoft's Virtual Machine Platform, which uses a subset of Hyper-V architecture.
- `PowerShell` = command-line shell and scripting language available on Windows, Linux, and macOS. On Windows, it can invoke Linux commands through WSL or SSH and run tools such as the Docker CLI.
- `shell` = command-line interpreter such as bash, zsh, or PowerShell.
- `Docker Desktop` = Docker application for Windows, Linux and macOS that provides Docker Engine, Docker CLI integration, and a GUI. It uses a Linux virtualization layer to run Linux containers: typically WSL 2 on Windows and a Linux VM on macOS.
- APT = **Advanced Package Tool**. It is Ubuntu/Debian's package management system. `apt` means: use APT to install some package interactively.
```text
APT
├── apt-get → install/update packages
└── apt     → newer, more user-friendly command, for interactive use
```
- Daemon = background process that runs continuously and handles requests. The Docker Engine daemon is called `dockerd`.
- Ubuntu Packages Search: https://packages.ubuntu.com/


## Useful interactive container commands

- `docker start -ai docker-walkthrough` → starts the stopped container and attaches to it interactively.
- `cd /app` → move to the application directory.
- `export VENV=/opt/venv` → set the virtual environment location.
- `export PATH="$VENV/bin:$PATH"` → add the virtual environment's `bin` directory to the `PATH` so that Python and pip from the virtual environment are used by default.
- `docker stop docker-walkthrough` → stops the container when you are done. Do not forget it, it will **NOT** be done automatically
- `docker rm docker-walkthrough` → removes the stopped container named `docker-walkthrough`.
