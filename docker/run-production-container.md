# Run the production container

For the CUDA image (powershell):

```powershell
docker run `
    --name test1-container `
    --gpus all `
    --cap-drop=ALL `
    --security-opt=no-new-privileges `
    -p 127.0.0.1:8501:8501 `
    test1-image
```

For the CPU-only image, remove:

```text
--gpus all
```

The Dockerfile `CMD` starts Streamlit automatically. Do not add `bash` to this production command. If you add `bash`, it replaces the Dockerfile `CMD`.

`--gpus all` gives the container access to the available NVIDIA GPUs. Docker requires the GPU to be explicitly made available to the container (https://docs.docker.com/reference/cli/docker/container/run). Docker also supports removing Linux capabilities with `--cap-drop`; `ALL` removes all of them.

* `run` → creates and starts a container from the image.
* `--name test1-container` → gives the container a readable name.
* `--gpus all` → gives the container access to all available NVIDIA GPUs.
* `--cap-drop=ALL` → removes all Linux capabilities from processes in the container. This will prevent the container from performing administrative operations that are normally allowed for root.
* `Linux capability` → a specific administrative permission that Linux can give to a process.
* `--security-opt=no-new-privileges` → prevents a process from gaining additional privileges when it starts another program.
* `privilege` → permission to perform an operation that a normal user cannot perform.
* `-p 127.0.0.1:8501:8501` → publishes Streamlit only on the local host, as explained earlier. Docker warns that omitting the host address can publish the port on all host network interfaces.
* `test1-image` → the image that you built.
* There is no `bash` at the end → Docker uses the Dockerfile `CMD` and starts Streamlit.

> After the first final build, test one Kaleido image export with these security options. Do **not** solve a Chrome problem by adding `--no-sandbox`; Chromium states that this disables important browser security protections. 

- Healthcheck: https://docs.docker.com/reference/dockerfile/#healthcheck