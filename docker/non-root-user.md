# Create a non-root user

Dockerfile:

```dockerfile
RUN useradd -m -u 1000 appuser \
    && mkdir -p /home/appuser/.cache/huggingface \
    && chown -R appuser:appuser /home/appuser
```

* `\` → continues the Dockerfile command on the next line.
* `&&` → runs the next command only if the previous command succeeds.

> Do **not** change ownership of `/app` to `appuser` in production. The application code in `/app` should remain owned by `root`, while the application itself runs as the non-root `appuser`.

> This is because if `appuser` owns `/app`, a compromised application process could modify its own code. Keeping `/app` owned by `root` means `appuser` can usually read and execute the code, but cannot replace or delete it. That reduces persistence and tampering risk. 

Interactively:

## Create the `appuser` user

```bash
useradd -m -u 1000 appuser
```

> Creates the `appuser` user with UID `1000`. UID `1000` is commonly used for a normal Linux user and can simplify permissions for bind-mounted files when the host uses the same UID.

* `useradd` → creates a user.
* `-m` → creates the user's home directory.
* `-u 1000` → sets user ID `1000`.
* `appuser` → name of the new user.

You can confirm the user and its groups with:

```bash
id appuser
```

For example:

```text
uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
```

* `uid` → user ID.
* `gid` → primary group ID.
* `groups` → groups to which the user belongs.

## Create the Hugging Face cache directory

```bash
mkdir -p /home/appuser/.cache/huggingface
```

* `mkdir` → creates a directory.
* `-p` → also creates missing parent directories and does not fail if the directory already exists.
* `/home/appuser/.cache/huggingface` → cache directory used by Hugging Face.

> `.cache` is hidden (dot prefix). Use `ls -a`.

## Give `appuser` ownership of its home directory

test the ownership of the directories:
```bash
ls -ld /home/appuser
ls -ld /home/appuser/.cache
ls -ld /home/appuser/.cache/huggingface
```

```bash
chown -R appuser:appuser /home/appuser
```

> `appuser` needs to be able to write to its home directory and cache directories.

* `chown` → changes file ownership.
* `-R` → applies the change recursively.
* `appuser:appuser` → sets the owner and group to `appuser`.
* `/home/appuser` → the user's home directory.

**Do not use:**

```bash
**chown -R appuser:appuser /app**
```

> `/app` contains the production application code. Keeping `/app` owned by `root` means `appuser` can read and run the application but cannot normally modify, delete, or replace its files.

test the ownership of the directories again:
```bash
ls -ld /home/appuser
ls -ld /home/appuser/.cache
ls -ld /home/appuser/.cache/huggingface
```

Before the `chown`, `/home/appuser` was typically already owned by `appuser` because `useradd -m` creates the home directory for that user.

But the extra cache directory you create as `root`:

```bash
mkdir -p /home/appuser/.cache/huggingface
```

can be root-owned. So:

```bash
chown -R appuser:appuser /home/appuser
```

ensures the whole home tree is consistently owned by `appuser`.

The Dockerfile later uses:

```dockerfile
USER appuser
```

> This controls which user runs the application. File ownership and process ownership are separate concepts: the files in `/app` can remain owned by `root` while the Streamlit process runs as `appuser`.

Running the application as a non-root user limits what the application process can do if it is compromised. Writable application data should go only to explicitly writable locations, such as `/home/appuser` or the mounted `/app/my-projects` directory.

## Configure Hugging Face cache

Dockerfile:

```dockerfile
ENV HOME=/home/appuser \
    XDG_CACHE_HOME=/home/appuser/.cache \
    HF_HOME=/home/appuser/.cache/huggingface
```

Interactively:

```bash
export HOME=/home/appuser
export XDG_CACHE_HOME=/home/appuser/.cache
export HF_HOME=/home/appuser/.cache/huggingface
```

Keeps user data and Hugging Face models/cache under the **non-root** user's home directory. `HF_HOME` is also where Hugging Face stores its local token by default. (https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables)

* `ENV` → sets environment variables in the image.
* `HOME` → sets the home directory for `appuser`.
* `XDG_CACHE_HOME` → sets the general user cache directory.
* `HF_HOME` → sets the Hugging Face data and cache directory.

> Do not put `HF_TOKEN` directly in the Dockerfile.