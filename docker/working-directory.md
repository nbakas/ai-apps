# Set the working directory

Dockerfile:

```dockerfile
WORKDIR /app
```

sets `/app` as the current directory and creates it if it does not exist.

> `/app` will contain your application files, such as the Python code, requirements, and any files copied into the image.

> `WORKDIR` also sets the working directory for later `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions.

Interactively:

first run:

`ls /` → lists the contents of `/` so you can see that `/app` does not exist.

Then run:

`mkdir -p /app` → creates `/app` interactively if needed.

* `mkdir` → creates a directory.
* `-p` → creates parent directories if needed and does not return an error if the directory already exists.

Run:

`ls /` → lists the contents of `/` again so you can see that `/app` has been created.

Then run:

`cd /app` → moves into `/app`.

Run:

`pwd` → shows the current working directory.

You should see:

```text
/app
```
