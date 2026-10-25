# Installing AI Apps

## Overview

This guide will:

- Make a folder ai-apps-main in your home folder.
- Download the AI Apps repository as a tarball, extract it into the folder and delete the tarball. 
- A second download overwrites files but does not remove obsolete files.
- Build the production Docker image.
- Pull the `nginx-unprivileged` image.
- Create the model's volume.
- Download a Hugging Face model.
- Download the llama cpp server image.
- Compose and run the container.

> Docker automatically creates `ai-apps-projects` if missing and mounts it at `/app/my-projects`.

Your project files will be in:

- Windows: `C:\Users\<user>\ai-apps-projects`
- macOS: `/Users/<user>/ai-apps-projects`
- Linux: `/home/<user>/ai-apps-projects`.
    - `ai-apps-projects` must be writable by UID 1000. Before starting the installation, create `~/ai-apps-projects` and ensure UID 1000 has write permission.

---
> By installing and using AI Apps, you agree to the [LICENSE.md](../LICENSE.md)
---

## Download and Install Docker Desktop

https://www.docker.com/products/docker-desktop/

> **Secure Docker Desktop**: Go to `Settings > Resources > Network > Port binding behavior` and ensure it is set to `Localhost only`! 


## All commands instructions

### Windows

Open a Command Prompt (type `cmd` in the Start menu and press Enter).

```
cd %USERPROFILE%
curl -fL -o ai-apps.tar.gz https://github.com/nbakas/ai-apps/archive/refs/heads/main.tar.gz
tar -xzf ai-apps.tar.gz
del ai-apps.tar.gz
cd ai-apps-main\production
docker build --pull --no-cache -f Dockerfile.prod -t ai-apps-prod-image .
docker pull nginxinc/nginx-unprivileged:stable-alpine-slim
docker volume create hf-cache
docker run --rm -t -v "hf-cache:/home/appuser/.cache/huggingface" ai-apps-prod-image hf download unsloth/Qwen3.5-0.8B-GGUF Qwen3.5-0.8B-Q4_K_M.gguf mmproj-F16.gguf --revision 6ab461498e2023f6e3c1baea90a8f0fe38ab64d0
docker pull ghcr.io/ggml-org/llama.cpp:server
docker compose -f docker-compose-prod.yaml up -d
```

### Linux / macOS

Open a terminal (Linux: `Ctrl+Alt+T`, macOS: `Cmd+Space`, type Terminal, press Enter).

```
cd ~
curl -fL -o ai-apps.tar.gz https://github.com/nbakas/ai-apps/archive/refs/heads/main.tar.gz
tar -xzf ai-apps.tar.gz
rm ai-apps.tar.gz
cd ai-apps-main/production
docker build --pull --no-cache -f Dockerfile.prod -t ai-apps-prod-image .
docker pull nginxinc/nginx-unprivileged:stable-alpine-slim
docker volume create hf-cache
docker run --rm -t -v "hf-cache:/home/appuser/.cache/huggingface" ai-apps-prod-image hf download unsloth/Qwen3.5-0.8B-GGUF Qwen3.5-0.8B-Q4_K_M.gguf mmproj-F16.gguf --revision 6ab461498e2023f6e3c1baea90a8f0fe38ab64d0
docker pull ghcr.io/ggml-org/llama.cpp:server
docker compose -f docker-compose-prod.yaml up -d
```

## Browser

The application should now be running in the Docker container.

Open http://localhost:8501 in your web browser.

## Stop and restart the container

Docker Desktop UI:

- To stop the container, go to Containers, click the stop button.
- To restart the container, click the start button.

Stop/restart the whole stack named `ai-apps-prod-container`, not one nested container.

Terminal:

- To stop the container:

```
docker compose -f docker-compose-prod.yaml stop
```

- To restart the container:

```
docker compose -f docker-compose-prod.yaml restart
```

## Step-by-step Installation

### Windows

```
cd %USERPROFILE%
curl -fL -o ai-apps.tar.gz https://github.com/nbakas/ai-apps/archive/refs/heads/main.tar.gz
tar -xzf ai-apps.tar.gz
del ai-apps.tar.gz
cd ai-apps-main\production
```

- `cd %USERPROFILE%`: go to the user's home folder `C:\Users\<user>`.
- `curl`: the download tool.
- `-f`: fail on an HTTP error. Without it, curl saves the error page as the file.
- `-L`: follow redirects. GitHub handles your request, then redirects it to `codeload.github.com`.
- `-o ai-apps.tar.gz`: save the download with this file name (in the current directory).
- `tar`: the archive tool.
- `-x`: extract.
- `-z`: unzip the gzip compression (`.gz`).
- `-f ai-apps.tar.gz`: the archive file to read.
- `del ai-apps.tar.gz`: delete the archive after extraction.
- `cd ai-apps-main\production`: enter the production directory within the extracted repository.

### Linux / macOS

```
cd ~
curl -fL -o ai-apps.tar.gz https://github.com/nbakas/ai-apps/archive/refs/heads/main.tar.gz
tar -xzf ai-apps.tar.gz
rm ai-apps.tar.gz
cd ai-apps-main/production
```

- `cd ~`: go to the user's home folder. `~` is `/home/<user>` (Linux) or `/Users/<user>` (macOS).
- `curl -fL -o` and `tar -xzf`: same as Windows.
- `rm ai-apps.tar.gz`: delete the archive after extraction.
- `cd ai-apps-main/production`: enter the production directory within the extracted repository.

### Build Docker Image

```
docker build --pull --no-cache -f Dockerfile.prod -t ai-apps-prod-image .
```

### Pull the `nginx-unprivileged` image:

```
docker pull nginxinc/nginx-unprivileged:stable-alpine-slim
```

### Create the model's volume

Create a Docker volume used to store the local model files:

```
docker volume create hf-cache
```

### Download a model

Download the pinned LLM files into the Docker model volume:

https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF
```
docker run --rm -t -v "hf-cache:/home/appuser/.cache/huggingface" ai-apps-prod-image hf download unsloth/Qwen3.5-0.8B-GGUF Qwen3.5-0.8B-Q4_K_M.gguf mmproj-F16.gguf --revision 6ab461498e2023f6e3c1baea90a8f0fe38ab64d0
```

You may change the model or revision as needed.

### Download llama cpp server image

For CPU inference:

```
docker pull ghcr.io/ggml-org/llama.cpp:server
```

### Compose the container

```
docker compose -f docker-compose-prod.yaml up -d
```

