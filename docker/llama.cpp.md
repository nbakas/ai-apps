# llama.cpp server image

For CPU inference:

powershell:
```powershell
docker run --rm aquasec/trivy image --scanners vuln --format table --table-mode detailed --severity HIGH,CRITICAL ghcr.io/ggml-org/llama.cpp:server
```

```powershell
docker pull ghcr.io/ggml-org/llama.cpp:server
```

For NVIDIA GPU inference:

powershell:
```powershell
docker run --rm aquasec/trivy image --scanners vuln --format table --table-mode detailed --severity HIGH,CRITICAL ghcr.io/ggml-org/llama.cpp:server-cuda
```

```powershell
docker pull ghcr.io/ggml-org/llama.cpp:server-cuda
```