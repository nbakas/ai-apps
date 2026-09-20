# Install Basic dependencies

Dockerfile snippet:

```dockerfile
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*
```

* `&&` → runs the next command only if the previous command succeeds.
* One `RUN` → keeps update, upgrade, install, and cleanup in the same image layer, avoiding stale package lists and unnecessary leftover files.

## Updated package index

Run `apt-get update` to refresh the APT package index before installing or upgrading software.

`apt-get update`

The APT package index contains information about available packages and versions from the configured repositories.

## Upgrading installed packages

`apt-get upgrade -y`

Upgrades already installed packages to the newest versions available from the current package repositories.

* `apt-get upgrade` → upgrades installed packages.
* `-y` → automatically answers yes to APT confirmation prompts.

> `apt-get update` only refreshes package information. It does not upgrade installed packages.

> `apt-get upgrade -y` is included to install available security and bug-fix updates from the Ubuntu repositories at build time. This means rebuilding the same Dockerfile later can install newer package versions.

## Checking installed packages

`dpkg -l`

Lists packages known to the `dpkg` database and their installation status.

* `dpkg` → package manager used by Debian-based systems such as Ubuntu.
* `-l` → lists packages and their installation status.

You will see a table with columns:

* `Status` → package installation status. For example, `ii` means the package is installed and configured.
* `Name` → package name.
* `Version` → installed version.
* `Architecture` → e.g. `amd64`.
* `Description` → package purpose.

If the output is displayed through a pager, you may see `--More--`.

> Press **Space** for the next page or **q** to exit.

> You can already see that the NVIDIA CUDA base image contains Ubuntu system packages plus CUDA packages such as `cuda-cudart-12-8` and `cuda-libraries-12-8`.

## `--no-install-recommends`

The three dependency relationships relevant here are:

* **Depends**: mandatory dependencies required by the package.
* **Recommends**: packages normally installed because they are useful with the package, unless you pass `--no-install-recommends`.
* **Suggests**: optional packages that are not installed by default.

In containers we often omit recommends to reduce image size and unnecessary packages.

## Installing GNU OpenMP runtime

`apt-get install -y --no-install-recommends libgomp1`

Installs the GNU OpenMP runtime library, which is used by software that runs parallel CPU operations.

* `libgomp1` → GNU OpenMP runtime library used by some compiled scientific and machine-learning packages for parallel CPU execution. `libgomp1` is needed by programs that were compiled with **GNU OpenMP** support.

Typical examples are scientific/ML libraries that use multiple CPU threads internally, such as parts of:

* NumPy / SciPy
* scikit-learn
* XGBoost / LightGBM
* other C/C++ numerical libraries

So it is **not for Python itself**. It is a runtime library that some compiled Python packages may depend on.

## Cleaning the APT package lists

`rm -rf /var/lib/apt/lists/*`

Removes the local files that APT downloaded when you ran `apt-get update`.

Those files contain information such as:

* package names
* available versions
* dependencies
* which repository each package comes from

APT uses that information to know what can be installed. After the packages are installed, these downloaded index files are no longer needed in the final image.

* `rm` → removes files and directories.
* `-r` → removes directories recursively.
* `-f` → removes without prompting and ignores nonexistent files.
* `/var/lib/apt/lists/*` → the downloaded APT package-index files.

> This reduces image size. It does not remove installed packages.