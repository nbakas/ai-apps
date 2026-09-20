# Base Images

## GPU

Interactively:

```powershell
docker pull nvidia/cuda:12.8.1-runtime-ubuntu24.04
```

This downloads the Ubuntu 24.04 + CUDA 12.8.1 runtime base image. 

In Dockerfile:

```dockerfile
FROM nvidia/cuda:12.8.1-runtime-ubuntu24.04
```

## CPU

Interactively:

```powershell
docker pull python:3.12-slim
```

In Dockerfile:
```dockerfile
FROM python:3.12-slim
```

## Linux Distributions

- Docker Desktop has no default OS to give you. 
- A container image contains filesystem layers and configuration, and it can carry its own distribution userland inside it.
- `FROM python:3.12-slim` means "start from an image whose filesystem is Debian with Python installed".
- Your host could be Windows, macOS, or Fedora — irrelevant, because the container brings its own userland.
- A base image carries the user-space filesystem: libraries, package manager, shell, utilities. Containers share the host/VM Linux kernel.

> What is shared is the host kernel on native Linux, or the Linux VM's kernel when using Docker Desktop.

So Debian vs Ubuntu in Docker mainly means different user-space packages and repositories, not separate kernels.