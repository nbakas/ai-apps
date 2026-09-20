# Interactive container

```powershell
docker run -it --name docker-walkthrough python:3.12-slim bash
```

Creates and starts an interactive container from the Python CPU base image and opens a Bash shell inside it.

* `-i` → keeps standard input open.
* `-t` → provides an interactive terminal.
* `--name docker-walkthrough` → gives the container a readable name.
* `python:3.12-slim` → image name and tag.
* `bash` → starts the Bash shell inside the container.

You will see a prompt like:

`root@<container-id>:/#`

Shows the current user, the container hostname, which defaults to the container ID, and the current working directory inside the container.

> To stop the container, type `exit`. The container will stop and you will return to your host shell.

You can restart it later with

```powershell
docker start -ai docker-walkthrough
```

* `start` → starts the stopped container.
* `-a` → attaches to it.
* `-i` → keeps it interactive.

After you stop and restart the container, you need to run the export commands again:

```bash
export VENV=/opt/venv
export PATH="$VENV/bin:$PATH"
```

Also, if you created `/app` interactively, you need to `cd /app` again.

```bash
cd /app
```

## Checking the container filesystem

```bash
ls
```

Lists the files and directories in the current directory. You will notice that only container files are visible, not host files.

> The container is isolated from the host filesystem unless host files are explicitly mounted.

## Container OS

WSL 2 is the **virtualization/Linux layer on Windows**, but the container itself uses the operating system provided by its image:

```text
python:3.12-slim
```

To check the exact distribution and version used by the current image:

```bash
cat /etc/os-release
```

`python:3.12-slim` is Debian-based.

> Debian-based images use the APT package system, so we can use `apt-get` to install and update software and `dpkg` to inspect installed packages.
