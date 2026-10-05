# `.dockerignore`



> Check thoroughly - anything not ignored here will be sent to the Docker build context!

```text
.git
__pycache__/
**/__pycache__/
*.pyc
*.pyo
.venv/
venv/
.env
user_data/
.cache/
*.log
.DS_Store
Thumbs.db
```

There is no interactive equivalent. `.dockerignore` is used only when Docker builds the image.

It prevents files that are not required by the application from entering the Docker build context and therefore from being copied by:

```dockerfile
COPY --chown=appuser:appuser . .
```

Docker recommends using `.dockerignore` to remove files that are not required during the build. (https://docs.docker.com/build/building/best-practices/)

* `.git` → excludes the local Git repository data.
* `__pycache__/` → excludes a Python cache directory at the project level.
* `**/__pycache__/` → excludes Python cache directories below other directories.
* `*` → matches any sequence of characters.
* `*.pyc` → excludes compiled Python cache files.
* `*.pyo` → excludes optimized Python cache files.
* `.venv/`, `venv/` → exclude local Python virtual environments. The container uses `/opt/venv`.
* `.env` → prevents a local environment file from entering the image. Do not store secrets in the image.
* `user_data/` → prevents local user data from entering the production image. Mount this directory separately if production needs it.
* `.cache/` → excludes local cache files.
* `*.log` → excludes log files.
* `.DS_Store` → excludes macOS directory-information files.
* `Thumbs.db` → excludes Windows thumbnail-information files.
* `/` at the end of a pattern → identifies a directory.

> `.dockerignore` affects the **Docker build**. It does not prevent a bind mount or `docker cp` from making a file available inside a running container.
