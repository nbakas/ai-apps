# Build the image

> Change `ai-apps-dev-image` to the name that you want for your image.

> The first two commands are a **hard stop**. They prevent the build if an image named `ai-apps-dev-image` already exists.

There is no equivalent command inside the walkthrough container. Docker Engine builds the image from the Dockerfile.

From the host, in the directory that contains the Dockerfile (powershell):

```powershell
docker image inspect ai-apps-dev-image *> $null
if ($LASTEXITCODE -eq 0) {
    throw "Image ai-apps-dev-image already exists. Choose another image name or remove the existing image."
}
```

* `docker image inspect ai-apps-dev-image` → checks if the image exists.
* `*> $null` → sends all output from the check to `$null`, so PowerShell does not show it.
* `$null` → a special PowerShell value used to discard output.
* `$LASTEXITCODE` → the exit code from the last external program, here `docker`.
* `-eq 0` → tests if the exit code is `0`. An exit code of `0` means that Docker found the image.
* `if (...) { ... }` → runs the commands between `{` and `}` only if the test is true.
* `throw` → stops the PowerShell command sequence and shows an error.

```powershell
docker build --pull --no-cache -f Dockerfile.dev -t ai-apps-dev-image .
```
* `docker` → Docker command-line program.
* `build` → builds an image from a Dockerfile.
* `--pull` → checks for a newer version of the referenced base image before the build.
* `--no-cache` → does not reuse results from an earlier Docker build.
* `cache` → stored results from earlier build steps that Docker can reuse.
* `-f Dockerfile.dev` → specifies the Dockerfile to use for the build.
* `-t` → gives the image a name and optional tag.
* `ai-apps-dev-image` → the image name. Because no tag is specified, Docker uses `latest`.
* `.` → uses the current directory as the Docker build context.
* `build context` → the files that Docker can use during the build. `.dockerignore` removes selected files from this context.


> A Docker image is immutable. You cannot edit it directly, however you can create a new image layer e.g.:

```Dockerfile
FROM existing-image:tag
RUN pip install package-name
```