# Security extras

## Secrets management

> Always put secrets outside project repo!

## Data Management

> Always put project data outside project repo!

## System and Network Security

- Ensure your operating system, firewall, antivirus software, and Docker Desktop are up to date and properly configured.
- In Docker Desktop → Settings → Resources → Network, set Port binding behavior to Localhost only to reduce accidental exposure of container ports to the local network or internet.
- Keep all applications and services accessible only through localhost, for streamlit: `-p 127.0.0.1:8501:8501`.
- When using docker-compose.yaml, bind every published port to localhost (`127.0.0.1:8501:8501`), drop all capabilities (`cap_drop: [ALL]`), set `no-new-privileges:true`, and use an `internal: true` network for services that need no internet.
- When using devcontainer.json, forward only the ports you need (`forwardPorts: [8501]`), set `remote.autoForwardPorts` to `false`, and run as a non-root user (`remoteUser`).

> Run the following command to list all running Docker containers:

```powershell
docker ps
```

> In the `PORTS` column, verify that you see `127.0.0.1:8501->8501/tcp`. This confirms that Docker publishes port 8501 to localhost only.

> If you see any other address (for example `0.0.0.0:8501` or `[::]:8501`), remove the container, then recreate it with `-p 127.0.0.1:8501:8501`.

## VSCode

When using devcontainer.json:

- Do not set `remote.localPortHost` to `allInterfaces`
- Do not set a forwarded port to Public
- Do not sign in to VS Code port forwarding or Remote Tunnels.

## Block outbound network

For runs that need no internet. 

```powershell
docker network create --internal dev-isolated
```

Add `--network dev-isolated` to `docker run`.

## More

- Run linters and formatters before commit, e.g. Ruff for Python.
- Run static security analysis, e.g. SonarQube for broader code-quality and security checks.
- Scan commits for accidentally committed secrets, e.g. Gitleaks.