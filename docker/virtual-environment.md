# Virtual environment

## Create the Python virtual environment

Dockerfile:

`ENV VENV=/opt/venv` → sets `/opt/venv` as the virtual-environment location.

`RUN python3 -m venv "$VENV"` → creates the virtual environment at `/opt/venv`.

`ENV PATH="$VENV/bin:$PATH"` → adds the virtual environment's `bin` directory to the `PATH` so that Python and pip from the virtual environment are used by default.

bash:

```bash
export VENV=/opt/venv
python3 -m venv "$VENV"
export PATH="$VENV/bin:$PATH"
```

Optional:

`echo $VENV` → verify the virtual environment location.

`echo $PATH` → verify that the virtual environment's `bin` directory is first in the `PATH`, so the virtual environment's Python/pip are used before the system ones.

Verify:

```bash
which python3
which pip
```

Expected:

```text
/opt/venv/bin/python3
/opt/venv/bin/pip
```

Notes:

* `-m` → runs a Python module as a script. There is no `venv` command on `PATH`; it lives inside Python. `-m` also guarantees the venv is built by that exact interpreter.
* `/opt` is the FHS (Filesystem Hierarchy Standard) location commonly used for optional/add-on software. It is a clean location for a self-contained virtual environment.
* The practical reason we use `/opt` instead of `/app`: if you bind-mount your source for development (`-v $PWD:/app`), the mount would shadow a venv stored inside `/app` and the container breaks. Keeping them separate means code and dependencies never collide.

## Verify the virtual environment

`ls -l /opt/venv/bin/python3`

* `ls` → shows the specified file.
* `-l` → uses long listing format to show detailed information about the file.

Run the command and read the actual output. The Python executable inside the virtual environment may be a symbolic link or a copied file, depending on how the virtual environment was created.

Typical symbolic-link output can look similar to:

```text
lrwxrwxrwx 1 root root 10 Aug 9 10:12 /opt/venv/bin/python3 -> python3.12
```

* `l` → file type: `l` = symbolic link, `-` = regular file, `d` = directory.
* `rwxrwxrwx` → permissions in three groups of three: owner, group, others.
* `r` = read, `w` = write, `x` = execute, `-` = not granted.
* `1` → number of hard links to the file.
* `root root` → First `root` is the user who owns the file, second `root` is the group that owns the file. Here, the file is owned by the `root` user and the `root` group.
* `10` → size in bytes. For a symbolic link, the length of the stored target path.
* `Aug 9 10:12` → last modification time.
* `->` → points to the link target.

> A symbolic link (symlink) is a file that contains the path of another file. Opening it opens the target instead, similar to a Windows shortcut but transparent: programs see the target's content. It is like a pointer, but it stores a name, not a memory address, and the name is resolved each time the file is opened. If the target is deleted, the symlink remains but breaks.

> A virtual environment has its own `site-packages` directory for pip installs. The Python executable inside the virtual environment may be linked to or copied from the base interpreter.
