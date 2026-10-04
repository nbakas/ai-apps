
# Start the Streamlit application

Dockerfile:

```dockerfile
CMD ["python", \
    "-m", \
    "streamlit", \
    "run", \
    "app.py", \
    "--server.address=0.0.0.0", \
    "--server.port=8501", \
    "--server.fileWatcherType=none", \
    "--browser.gatherUsageStats=false", \
    "--browser.serverAddress=localhost", \
    "--server.headless=true"]
```

the walkthrough container must already have been started with:

```powershell
docker run -it --name docker-walkthrough -p 127.0.0.1:8501:8501 python:3.12-slim bash
```

Copy the Streamlit application file into the running container:
```powershell
docker cp app.py docker-walkthrough:/app/app.py
```

Interactively, in the walkthrough container:

```bash
test -f /.dockerenv && \
python -m streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.fileWatcherType=none \
    --browser.gatherUsageStats=false \
    --browser.serverAddress=localhost \
    --server.headless=true
```

> **IMPORTANT: NEVER SKIP `test -f /.dockerenv &&` in this interactive command.** It checks for Docker's `/.dockerenv` file and starts Streamlit only if that file exists. This reduces the risk of accidentally running `--server.address=0.0.0.0` on the host. Inside the container, `0.0.0.0` makes Streamlit listen on all container network addresses. Host access is still limited by Docker with `-p 127.0.0.1:8501:8501`.

* `test -f` → checks that the specified path exists and is a regular file.
* `/.dockerenv` → a file that Docker normally creates inside a container. A normal host system does not **usually** have this file.
* `&&` → runs the next command only if the test succeeds.

> One important detail: `/.dockerenv` is a practical Docker check, **not a security guarantee**, because other container systems do not make this file, and a person can make the file on a host.

For **production and Hugging Face**, `CMD` starts Streamlit automatically when the container starts. For **development**, if you start the container with `bash`, that `bash` command replaces the Dockerfile `CMD`, so start Streamlit manually when you want it. Streamlit supports command-line configuration options in this form. (https://docs.streamlit.io/develop/concepts/configuration/options)

* `CMD` → sets the default command that runs when the container starts.
* `[ ]` → JSON array syntax used by Docker for the command and its arguments. Use the JSON array form `[ ]`. With the shell form (`CMD python -m streamlit ...`), Docker starts a shell as the main container process. Streamlit then runs as a child process. The shell might not pass stop signals correctly to Streamlit. The JSON array form runs Python directly as the main process, so it can receive Docker stop signals correctly.
* `python` → starts the Python interpreter from `/opt/venv` because the virtual-environment path is first in `PATH`.
* `-m` → runs an installed Python module.
* `streamlit` → the Python module to run.
* `run` → starts a Streamlit application. (https://docs.streamlit.io/develop/api-reference/cli/run)
* `app.py` → the Streamlit application file.
* `--server.address=0.0.0.0` → makes Streamlit listen on all network addresses inside the container so Docker can forward connections to it.
* `--server.port=8501` → makes Streamlit listen on container port `8501`.
* `--server.fileWatcherType=none` -> disables source-file watching. This is appropriate for the production image, where the application files do not change.
* `--browser.gatherUsageStats=false` → disables Streamlit usage-statistics collection. 
* `--server.headless=true` → prevents Streamlit from trying to open a browser and from asking for an email address at the first start. A container has no graphical display. (https://docs.streamlit.io/develop/api-reference/configuration/config.toml)

> Streamlit uses `--server.address=0.0.0.0` inside the container. `0.0.0.0` means all network interfaces. This is necessary, because the container has its own network. If Streamlit binds to `127.0.0.1` inside the container, Docker cannot send your request to it. The protection is the `127.0.0.1` in the `-p` option on the host.

```text
0.0.0.0 in the container  → Streamlit accepts the request from Docker
127.0.0.1 on the host     → only your machine can send a request
```
> Streamlit must listen on `0.0.0.0` inside the container so that the Docker port mapping can reach it. `0.0.0.0` means: listen for connections on all network addresses inside the container.

> For a container without live source editing, use:
```dockerfile
"--server.fileWatcherType=none",
```
`poll` repeatedly checks files; `none` disables watching entirely.