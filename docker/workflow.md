# Workflow

The end-to-end workflow: from a list of Python packages to a hardened, localhost-only Streamlit app that chats with a local LLM.

```text
requirements.in
      |
      v
`uv` -->  requirements.txt
      |
      v
Build images (Dockerfile.dev, Dockerfile.prod)
      |
      v
Scan images (Trivy)
      |
      v
Get the model (Hugging Face GGUF) + llama.cpp server image
      |
      v
Deploy (Docker Compose: app + llama + proxy)
      |
      v
Verify (run streamlit, check 127.0.0.1:8501)
```

## 1. Lock dependencies

Docs: [Hardened Python Packages Installations](installations-uv.md)

- Edit `requirements.in` by hand (package names only).
- Make `requirements.txt` with `uv pip compile` (hashes, binary-only, cooldown). Do not edit it by hand.

## 2. Build images

Docs: [Base Images](base-images.md), [Virtual Environment](virtual-environment.md), [Non-root user](non-root-user.md), [.dockerignore](dockerignore.md), [Build the image](build-the-image.md)

Files: [Dockerfile.dev](../development/Dockerfile.dev), [Dockerfile.prod](../production/Dockerfile.prod)

## 3. Scan images

Docs: [Scanning for vulnerabilities with Trivy](trivy.md)

- Save each image to a `.tar` file and scan it with the digest-pinned Trivy image.

## 4. Get the model

Docs: [Hugging Face models volume](huggingface-models-volume.md), [llama.cpp server image](llama.cpp.md)

- Select a GGUF model (`.gguf` file, `mmproj` file, quantization such as `Q4_K_M`).
- Download it into the `hf-cache` Docker volume.
- Pull the llama.cpp server image (`:server` for CPU, `:server-cuda` for NVIDIA GPU).

## 5. Deploy

Docs: [Run the production container](run-production-container.md), [Security](security.md)

Files: [docker-compose-prod.yaml](../production/docker-compose-prod.yaml)

- Services: `app` (Streamlit), `llama` (llama.cpp server), `proxy` (Nginx, the only published port).
- `docker ps` must show `127.0.0.1:8501`, not `0.0.0.0`.

## 6. Verify

Files: [app.py](../app.py)

- Open `http://127.0.0.1:8501` and chat with the model.