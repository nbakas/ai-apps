
# Run the development container

Interactively (after you build the image with the Dockerfile):

```powershell
docker run -it `
    --name test1-dev-container `
    --gpus all `
    --user appuser `
    --cap-drop=ALL `
    --security-opt=no-new-privileges `
    -p 127.0.0.1:8501:8501 `
    -v "${PWD}:/app" `
    test1-image `
    bash
```

For the CPU-only image, remove:

```text
--gpus all
```

> IMPORTANT: The `${PWD}` variable represents the current working directory on the host. Make sure you run the `docker run` command from a folder with the project files only!

Inside the container:

```bash
python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.fileWatcherType=poll --browser.serverAddress=localhost --browser.serverPort=8501 --browser.gatherUsageStats=false --server.headless=true
```

To stop Streamlit, press `Ctrl+C` in the container terminal. 

Then exit the container with `exit`. The container stops.


After first run, restart the existing container:

```powershell
docker start -ai test1-dev-container
```

Then run the Streamlit command again inside. The full `docker run` command would fail because the container name already exists.

> For development, use a bind mount so the host project replaces `/app` while the container runs.

> During **local development**, the bind mount makes your host project available at `/app` inside the container.

> `"${PWD}:/app"` hides the files that the Dockerfile copied into `/app` while that container is running. 

> Changes that you save on the host are therefore immediately visible inside the container.

> The virtual environment is at `/opt/venv`, not in `/app`. Therefore the mount does not hide the installed packages.

* `-it` → keeps standard input (`i`) open and provides an interactive terminal (`t`).
* `--name test1-dev-container` → gives the container a readable name.
* `-p 127.0.0.1:8501:8501` → maps port 8501 on the host to port 8501 in the container (port bind). 
* `port bind` → makes a program or a published port use a specified network address. Here, Docker binds host port `8501` to `127.0.0.1`.
* `-v` → creates a bind mount.
* `bind mount` → makes a host file or directory available at a specified path inside the container.
* `"${PWD}:/app"` → mounts the current host project directory at `/app` inside the container.
* `:` → separates the host path from the container path.
* `<image-name>` → replace with the image name that you built.
* `bash` → opens an interactive Bash shell. `bash` command replaces the Dockerfile `CMD`, so start Streamlit manually when you want it.

> Caution: this is not the same as a bind mount. A bind mount shares a directory. A port bind connects a port to a network address.

* `-p 127.0.0.1:8501:8501`    → port bind     (connects a port to an address)
* `-v "${PWD}:/app"`          → bind mount    (shares a directory)

## Port mapping

`-p 127.0.0.1:8501:8501`

* `-p` → publishes (makes the container port available) through a host port. Maps a port on the host to a port in the container.
* `127.0.0.1` → the IPv4 (Internet Protocol version 4) loopback address of the host. The operating system kernel treats `127.0.0.1` as a loopback address (a network address used for communication inside the same computer). Network traffic to this address does not leave the computer. Accordingly, `localhost` is the standard name for the local computer address, `localhost` usually uses `127.0.0.1` for IPv4.
* first `8501` → the port on the host. `port` is a number that identifies a network connection used by a program. In total, 65535 ports exist for one address (here, the host - `127.0.0.1`). Port numbers are from 0 to 65535. Port 0 has a special purpose (if a program asks the operating system to use port 0, the operating system chooses an available port number for that program.), so applications normally use ports 1 to 65535.
* second `8501` → the port inside the container. 
* Both are `8501` → the host port and the container port can have the same number. This is convenient, but it is not necessary. For example, `9000:8501` connects host port `9000` to container port `8501`.
* `127.0.0.1:8501:8501` → **host address : host port : container port**.

> Flow

Docker publishes host port `8501`. Streamlit listens on port 8501 inside the container. `listens` means a program waits for network connections on a specified port. Nothing listens on container port 8501 yet. Docker creates the port mapping from host port `8501` to container port `8501`. Docker does not start a program on the container port. Streamlit must listen on that port. When you start Streamlit, it will listen on container port 8501. Streamlit listens for **network connections that arrive at the container’s port `8501`**. It does not listen “from the host” directly. Docker can do this because the Docker Engine has high system privileges. Docker connects the host port to the container port. `127.0.0.1` limits the host port to the local computer only.

`host browser → host port 8501 → Docker port mapping → container port 8501 → Streamlit process`

So Streamlit only listens inside the container. Docker forwards the host connection to it.

* `exposed to the network` → other computers can connect to the port through the network.
* Because Docker binds the port to `127.0.0.1`, other computers cannot normally connect to it. Only programs on the host can connect to it.

## Restart the development container

PowerShell:

```powershell
docker stop test1-dev-container
docker start -ai test1-dev-container
```

> `docker start` starts the **same container** with the settings that were specified when `docker run` created it. This includes the port mapping, `--cap-drop=ALL`, `--security-opt=no-new-privileges`, GPU access, and environment variables.

* `docker stop` → stops the running container without deleting it.
* `docker start` → starts the existing stopped container.
* `-a` → attaches your terminal to the container output.
* `-i` → keeps standard input open.
* `test1-dev-container` → the existing container name.

> If you remove the container, files stored only inside it are deleted. Files in bind mounts or Docker volumes remain.