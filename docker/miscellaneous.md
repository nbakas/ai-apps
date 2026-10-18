# Miscellaneous

This section covers various miscellaneous topics related to Docker and the development environment.


## Git files

`.gitattributes`:

```text
* text=auto eol=lf
```

`text=auto` means that Git will handle line endings automatically, and `eol=lf` ensures that line endings are normalized to LF (Line Feed i.e., `\n`) in the repository.

`.gitignore`:

```text
__pycache__/
*.py[cod]
...
```

Git runs on Windows, never inside the container.

## Make the Dockerfile

You can use the python script `make_dockerfile.py`, to generate the Dockerfile.

```powershell
docker run --rm -it -v "${PWD}:/work" -w /work python:3.12-slim bash
```

```bash
python make_dockerfile.py
```

- copy the `Dockerfile` to the project root.
- press `exit` to stop the container if it is running.
