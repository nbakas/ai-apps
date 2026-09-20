# Virtualization stack

## Windows 11

```
Hyper-V virtualization technology      → provides VM isolation
│
├── Windows 11
│   └── Windows kernel                 → runs Windows
│
└── WSL 2 virtualization               → runs Linux on Windows
    │
    └── Linux kernel                   → shared by WSL environments
        │
        ├── Ubuntu WSL                 → your Linux development environment
        │   └── Your Linux user        (docker CLI available here via
        │       └── VS Code terminal    Settings > Resources > WSL Integration)
        │
        └── Docker Desktop WSL backend
            └── Docker Engine      → builds images / runs containers
                └── Linux containers
```

dedicated Hyper-V VM = separate isolation architecture because it has its own Linux kernel

## Native Linux

```
Linux
│
├── Linux kernel                       → runs Linux and manages hardware
│
└── Docker Engine                      → builds images / runs containers
    │
    └── Linux containers               → run directly using the host Linux kernel
```

So on native Linux there is **no WSL 2 and no Hyper-V layer** between Docker and the Linux kernel.

## macOS

```text
macOS
│
├── macOS kernel                       → runs macOS and manages hardware
│
└── Docker Desktop VM                  → provides a Linux environment for Docker
    │
    └── Linux kernel                   → used by Linux containers
        │
        └── Docker Engine              → builds images / runs containers
            │
            └── Linux containers       → run inside the Docker Linux VM
```

## Security

> By default, a container inside that VM cannot simply browse `C:\Users\...` or your macOS files. Host files become accessible only through mechanisms such as bind mounts/file sharing. Even root inside the container cannot access unmounted Windows/macOS host files.

> Caveat: anyone able to run `docker` can create those mounts at will. On native Linux, access to the Docker daemon is equivalent to root access; Docker Desktop does not make Docker CLI access equivalent to Windows/macOS administrator privileges.

> Mounting the host root read-write, using `--privileged`, or mounting `/var/run/docker.sock` into a container can defeat this isolation. On native Linux, this can lead to host root access. On Docker Desktop, this can lead to root access inside the Linux VM plus access to host files that your own user can share.

> To avoid accidental conflicts and security issues, **DO NOT INSTALL PYTHON LOCALLY**.
