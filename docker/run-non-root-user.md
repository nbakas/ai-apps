
# Run as the non-root user

Dockerfile:

```dockerfile
USER appuser
```

Interactively, in the current walkthrough container:

```bash
su - appuser
```

> This changes the active user from `root` to `appuser`.

For **development and production**, run the application as `appuser`. Use `root` only when you must do an administrative task, such as installing a new package in `/opt/venv`.

* `USER` → sets the user for the Dockerfile instructions that follow it and for the container when it starts.
* `appuser` → the non-root user that you created.
* `su` → changes to another user.
* `-` → starts a login shell for the new user. It uses the new user's home directory and user environment. Without `-`, root's environment variables stay. A variable can give access that appuser does not have in reality. Example: `HF_TOKEN` from root stays available.
* `appuser` → the user to change to.

Verify interactively:

```bash
whoami
```

Expected:

```text
appuser
```

> Note: If you do `which python3`, you will get `/usr/bin/python3`, which is the system Python from the python3 apt package.

**After `su - appuser` in this walkthrough**, set the virtual-environment path again:

```bash
export VENV=/opt/venv
export PATH="$VENV/bin:$PATH"
```

Then verify:

```bash
which python3
```

Expected:

```text
/opt/venv/bin/python3
```

Important: this reset is needed because `su -` creates a new login environment. In the final Docker image, `USER appuser` does **not** remove the Dockerfile `ENV PATH=...`, so you do not need to set it again there.
