# Hardened Python Packages Installations

## Rationale

The goal is to:
- Install only pre-built binary wheels from PyPI. This reduces the risk of malicious code executing during package builds by allowing wheels only.
- Pin versions and hashes of all packages. The hash means: For this pinned package/version, accept only this exact file content. Hashes protect against a changed/tampered artifact or an unexpected file being downloaded. They are about file integrity and reproducibility.
- Use a cooldown to avoid installing packages that were released recently, as malicious uploads are usually removed from PyPI within days.

## Initial setup

> make `requirements.in` by hand (package names, no versions).

> `requirements.txt` will be generated. Never edit it.

Commit both.

## Install `uv`

We will use `uv` (https://github.com/astral-sh/uv), a fast Python package manager with a pip-compatible interface. It supports controls we will use for hardened installs.

Particularly, we will use:

- `--only-binary :all:` - blocks source distributions and builds, so `setup.py` never runs. Does not make a malicious wheel safe.
- `--require-hashes` - requires every dependency to be exactly pinned and to have a matching hash; the hash verifies the downloaded distribution file.
- `--exclude-newer "7 days"` - cooldown; malicious uploads are usually removed from PyPI within days.

> Note: `--only-binary` and `--require-hashes` are concepts supported by pip too, however `uv` is faster and `--exclude-newer` is a useful uv resolver feature.


Dockerfile:

```dockerfile
RUN pip install --no-cache-dir --only-binary=:all: uv pip-audit
```

Interactively:

```powershell
pip install --no-cache-dir --only-binary=:all: uv pip-audit
```

Then verify:

```powershell
uv --version
```


## Copy requirements.in host → container

Interactively, from **PowerShell**:

```powershell
docker cp requirements.in docker-walkthrough:/app/requirements.in
```

- `docker cp` → copies a file between the host and a container.

> **Note:** Run `docker cp` from the host (PowerShell), not from inside the container.

## Generate the locked requirements.txt

`requirements.in` is maintained manually. Generate `requirements.txt` from it before building the final image.

**Dockerfile:** Do **not** run `uv pip compile` in the Dockerfile. The Dockerfile should consume the already-generated lock file:

> **Interactively, inside the container:**

```powershell
uv pip compile requirements.in \
    --generate-hashes \
    --only-binary=:all: \
    --exclude-newer "7 days" \
    -o requirements.txt
```

- `requirements.in` → package names and index configuration; edit manually.
- `--generate-hashes` - pins versions and verifies allowed distribution files by hash; may include multiple hashes per package/platform.
- `--only-binary :all:` - blocks source distributions and builds, so `setup.py` never runs. Does not make a malicious wheel safe.
- `--exclude-newer "7 days"` - cooldown; malicious uploads are usually removed from PyPI within days.
- `-o` - output file to write.
- `requirements.txt` → generated pinned dependencies and hashes; do not edit manually.
- Commit both files.

> Why does `requirements.txt` contain many packages?

`requirements.in` contains the packages that we select. `uv pip compile` also adds all packages that these packages depend on. Therefore, `requirements.txt` is much larger than `requirements.in`.

> Why does one package have many hashes?

One package version can have different wheel files for Linux, Windows, macOS, CPU architectures, and Python versions. Each file has its own hash. `uv` records the hashes of the allowed files and verifies the selected file during installation. Do not edit these hashes manually. The installer will select the correct wheel for the current platform and verify its hash: the pinned hash from `requirements.txt` with the hash of the downloaded file. If the hash does not match, the installation fails.

## Dockerfile: Copy requirements.txt host → container

**PowerShell the host**: then copy the generated file back to the host 

```powershell
docker cp docker-walkthrough:/app/requirements.txt .
```

```dockerfile
COPY requirements.txt .
```

- Copies `requirements.txt` from the Docker build context into the current working directory `/app`.
- `.` → means to the current Dockerfile working directory, which is `/app`.

## Audit the requirements file for known vulnerabilities

**Interactively, inside the container:**

```bash
pip-audit \
    --require-hashes \
    --disable-pip \
    -r requirements.txt
```

- `--require-hashes` → requires every dependency to be exactly pinned and to have a matching hash; the hash verifies the downloaded distribution file.
- `--disable-pip` → by default, pip-audit starts pip in a temporary environment. pip must find the dependencies of each package. To do this, pip downloads files. `--disable-pip` stops this. Your file is fully pinned and has all dependencies. Therefore resolution is not necessary. pip-audit reads the names and versions from the file, and asks the vulnerability database. Result: no download, no temporary environment, no hash error. It is also much faster.
- `-r` → tells `pip-audit` which requirements file to audit. Without `-r`, it audits the current Python environment instead.

> **Vulnerabilities:**

- `pip-audit` reports known vulnerabilities identified by vulnerability databases, such as Common Vulnerabilities and Exposures (CVE), GitHub Security Advisories (GHSA), and Python Security (PYSEC) identifiers. By default, it uses PyPI's vulnerability service. Google's Open Source Vulnerabilities (OSV) is also supported. It does not detect malicious packages or typosquats.
- The cooldown reduces exposure to newly published malicious packages, but does not guarantee safety.
- Run the container as non-root user, and do not run any code from untrusted sources. The container is not a sandbox.
- Run the container in localhost-only mode, and do not expose it to the internet.

In the Dockerfile, do:
```dockerfile
RUN pip-audit \
    --require-hashes \
    --disable-pip \
    -r requirements.txt
```

Vulnerability Databases:

- PYSEC: Python-specific security advisory identifier.
- CVE: Global standardized vulnerability identifier.
- alias = another vulnerability ID for the same security issue.

## Sync the requirements.txt file 

> This will install the pinned packages and verify their hashes. 

> If you later add a package to `requirements.in`, you will need to regenerate `requirements.txt` but `uv pip compile` resolves the dependencies. `uv pip sync` installs the exact packages from requirements.txt.

> To update packages during development, enter the running container as root with `docker exec -u root -it <container-name> bash`, then run `uv pip sync` or the required install command.

Interactively, inside the container:
```bash
uv pip sync requirements.txt \
    --require-hashes \
    --only-binary=:all:
```

In the Dockerfile, this is done in one line:
```dockerfile
RUN uv pip sync requirements.txt \
    --require-hashes \
    --only-binary=:all:
```

## Next: dependency check

Dockerfile

```dockerfile
# Check Python package compatibility
RUN uv pip check
```

Interactively:

```bash
uv pip check
```

It checks that all installed packages are compatible with each other and that there are no missing dependencies.

Expected:

```text
All installed packages are compatible
```