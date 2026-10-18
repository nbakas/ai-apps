# Hugging Face models volume

## Downloading models

Creates the `hf-cache` volume. Compose declares it `external: true`, so it will not start until this has run once.

Token stays outside the project, read-only. Never write its value here.

```powershell
docker run --rm -it `
    --mount "type=bind,source=C:/secrets/hf_token.txt,target=/run/secrets/hf_token,readonly" `
    --env HF_TOKEN_PATH=/run/secrets/hf_token `
    -v "hf-cache:/home/appuser/.cache/huggingface" `
    ai-apps-image `
    hf download <repository> <model.gguf> <mmproj.gguf>
```

e.g. 
- hf download unsloth/gemma-4-E2B-it-GGUF gemma-4-E2B-it-Q4_K_M.gguf mmproj-F16.gguf
- hf download unsloth/Qwen3.5-0.8B-GGUF Qwen3.5-0.8B-Q4_K_M.gguf mmproj-F16.gguf

## HF_TOKEN

`HF_TOKEN_PATH` tells Hugging Face where to read the authentication token file inside the container.

> **Note:** For public, non-gated models, omit the token mount `--mount "type=bind,..."` and `--env HF_TOKEN_PATH=/...`; authentication is not required.

## Model paths

Copy the `<printed-path>`. It goes into the yaml:

```yaml
llama:
  command: ["--model", "<printed-path>", ...]
```

- If you later want to download another model, repeat the download steps and update the `<printed-path>` in the yaml accordingly. 
- The same `hf-cache` volume keeps both models. 
- `--rm` removes the container; named volumes survive independently.

To find the paths of the downloaded models inside the `hf-cache` volume, run:

```powershell
docker run --rm -v "hf-cache:/home/appuser/.cache/huggingface:ro" --entrypoint find ai-apps-image /home/appuser/.cache/huggingface/hub -xtype f -name "*.gguf"
```

- `docker run` — Starts a temporary container.
- `--rm` — Removes the container after execution.
- `-v` — Mounts the existing `hf-cache` volume.
- `:ro` — Mounts the volume as read-only.
- `/home/appuser/.cache/huggingface` — Path inside the container where the Hugging Face cache is mounted.
- `--entrypoint find` — Runs `find` instead of the image's default entrypoint.
- `ai-apps-image` — Docker image to use.
- `/home/appuser/.cache/huggingface/hub` — Directory to search.
- `-xtype f` — Matches regular files and symbolic links pointing to regular files.
- `-name "*.gguf"` — Finds filenames ending in `.gguf`.

Result: Prints model paths that you can copy into your YAML, assuming the llama container uses the same mount path.