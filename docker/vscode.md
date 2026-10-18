# VS Code Development Container Configuration

## .devcontainer/docker-compose.yaml

-----
> For NVIDIA GPU inference: Use `ghcr.io/ggml-org/llama.cpp:server-cuda` and keep `--gpus all` for NVIDIA GPU inference.
-----
> For CPU inference: Use `ghcr.io/ggml-org/llama.cpp:server` and remove `--gpus all` 
-----


For GPU inference, add to `llama`: 

```yaml
image: ghcr.io/ggml-org/llama.cpp:server-cuda
gpus: all
command: ["--model", "...", "--host", "0.0.0.0", "--port", "8080", "--n-gpu-layers", "all"]
```

- `--n-gpu-layers` now accepts `auto`, `all`, or an exact number; default is `auto`
- `auto` fails if the model exceeds VRAM

In your Python code use `LLAMA_BASE_URL`, e.g.:

```python
import os
from openai import OpenAI
client = OpenAI(base_url=os.environ["LLAMA_BASE_URL"], api_key="not-used")
```

or any other code that needs to interact with the LLaMA server.

## .devcontainer/devcontainer.json

> Check the `.devcontainer/devcontainer.json` file for the correct VS Code development container configuration.

## Reopen in Container

After configuring the `.devcontainer` files, reopen the project in the container by selecting `Ctrl+Shift+P` → `Dev Containers: Reopen in Container` from the VS Code command palette.

## Running the Streamlit App

Inside the container:

```bash
python -m streamlit run app.py --server.address=127.0.0.1 --server.port=8501 --server.fileWatcherType=poll --browser.serverAddress=localhost --browser.serverPort=8501 --browser.gatherUsageStats=false --server.headless=true
```

> Note: In VS Code you can use `127.0.0.1` instead of `0.0.0.0` for the server address when running the Streamlit app. VS Code automatically forwards the port from inside the container, and that works, in contrast to interactive container.


## VS Code global settings

To configure VS Code global settings for the development container, edit the following file:

`C:\Users\<user>\AppData\Roaming\Code\User\settings.json`

```jsonc
{
  "dev.containers.copyGitConfig": false, // no host Git config in container
  "dev.containers.gitCredentialHelperConfigLocation": "none" // no credential bridge
}
```