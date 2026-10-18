# Security

> **Disclaimer:** The following security recommendations are general guidelines and may need to be adapted to your specific environment and threat model.

## Security main points

Main security controls:

- Run containers as a non-root user.
- Restrict containers to internal Docker networks.
- Expose Streamlit only through localhost.
- No secrets in the project repo.
- No sensitive data in the project repo.
- Use reputable base images, models and Python packages.
- No python on host, no VS Code extensions.

Additionally:

- Use `uv` with `--only-binary=:all:` to avoid source builds.
- Use `--exclude-newer "7 days"` to avoid very recent package releases that might not be reported as vulnerable yet.
- Scan container images with Trivy.
- Audit Python dependencies with `pip-audit`.
- `cap_drop: ALL` - drops all Linux capabilities from the container.
- `no-new-privileges:true` - prevents privilege escalation within the container.
- `--generate-hashes` + `--require-hashes` — pinned artifacts, so a re-uploaded or tampered wheel fails the install.
- `pull_policy: never` — prevents Compose from pulling a replacement image.
- `external: true` — you use the volume and the volume you filled. No silent substitution.
- no git inside the container and no git credential bridge
- VS Code extensions inside the container.
- Update Docker Desktop, VS Code, and extensions regularly.
- Re run the entire pipeline regularly for recent versions and vulnerability checks.
- Use Nuitka for production, no cloud server.

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

## Updates

> Revisit the pipeline to regularly update:

- Base images for CPU and GPU
- llama.cpp server image
- `requirements.in`
- Dockerfiles
- Containers
- VS Code and installed extensions

## More

- Run linters and formatters before commit, e.g. Ruff for Python.
- Run static security analysis, e.g. SonarQube for broader code-quality and security checks.
- Scan commits for accidentally committed secrets, e.g. Gitleaks.