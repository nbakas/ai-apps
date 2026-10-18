# Scanning images for known vulnerabilities with Trivy

## Save image to a tar file

```powershell
docker save -o C:\...\images\ai-apps-dev-image.tar ai-apps-dev-image:latest
```

## Download Trivy Image (alternative to installing Trivy on the host)

```powershell
docker pull aquasec/trivy
```

Downloads Trivy as a Docker image. Trivy is used to scan container images for known vulnerabilities. 

https://github.com/aquasecurity/trivy

https://trivy.dev/docs/latest/guide/target/container_image/

Get the digest of the Trivy image to ensure you are using the correct version.

```powershell
docker image inspect aquasec/trivy --format '{{json .RepoDigests}}'
```    

you will get an output similar to this:

```json
["aquasec/trivy@sha256:62b1....969"]
```

```powershell
$dockerArgs = @(
"run"
"--rm"
"--user"
"65532:65532"
"--cap-drop"
"ALL"
"--security-opt"
"no-new-privileges=true"
"--read-only"
"--tmpfs"
"/tmp:rw,noexec,nosuid,nodev,mode=1777"
"--mount"
"type=bind,source=C:\...\images\ai-apps-dev-image.tar,target=/scan/image.tar,readonly"
"aquasec/trivy@sha256:62b1e65e8869bc4b4c6aa4fa2b21595256c7c2f6018a9d9ad61caf87187c1969"
"image"
"--timeout"
"90m"
"--disable-telemetry"
"--skip-version-check"
"--no-progress"
"--format"
"table"
"--table-mode"
"detailed"
"--severity"
"HIGH,CRITICAL"
"--cache-dir"
"/tmp/trivy-cache"
"--input"
"/scan/image.tar"
)
[Console]::OutputEncoding = [Text.Encoding]::UTF8
docker @dockerArgs | Out-File "C:\...\images\trivy-scan-HIGH-CRITICAL.txt" -Encoding utf8
```

> To scan for secrets, remove the `--scanners`, `vuln`, `--severity` and `HIGH,CRITICAL` lines, below `image`, because `--severity HIGH,CRITICAL` also filters secret findings! You may need to increase the `--timeout` value for large images.

- `$dockerArgs = @(` - Creates a PowerShell argument array.
- `"run"` - Starts a new Docker container.
- `"--rm"` - Removes the container after exit.
- `"--user" "65532:65532"` - Runs as non-root user/group IDs.
- `"--cap-drop" "ALL"` - Removes all Linux capabilities.
- `"--security-opt" "no-new-privileges=true"` - Blocks privilege escalation.
- `"--read-only"` - Makes the container filesystem read-only.
- `"--tmpfs" "/tmp:rw,noexec,nosuid,nodev,mode=1777"` - Creates temporary writable memory-backed storage.
- `rw` - Allows writes to `/tmp` inside the Trivy container.
- `noexec` - Blocks direct execution from `/tmp`.
- `nosuid` - Disables set-user-ID/set-group-ID privilege effects.
- `nodev` - Blocks device-file use.
- `mode=1777` - Standard shared temporary-directory permissions.
- `"--mount"` - Defines a Docker mount.
- `type=bind` - Mounts a Windows host path.
- `source=...tar` - Your saved application image TAR.
- `target=/scan/image.tar` - TAR location inside the container.
- `readonly` - Prevents Trivy modifying the TAR.
- `aquasec/trivy@sha256:...` - Runs the exact digest-pinned Trivy image.
- `"image"` - Selects Trivy image scanning.
- `--scanners` - Specifies which types of scans to perform, e.g., `vuln` for vulnerability scanning.
- `"--disable-telemetry"` - Disables Trivy telemetry.
- `"--skip-version-check"` - Stops the update check request to check.trivy.dev.
- `"--no-progress"` - Disables progress output.
- `"--format" "table"` - Uses table output.
- `"--table-mode" "detailed"` - Shows detailed table information.
- `"--severity" "HIGH,CRITICAL"` - Displays only HIGH and CRITICAL findings.
- `"--cache-dir" "/tmp/trivy-cache"` - Stores temporary Trivy cache under `/tmp`.
- `"--input" "/scan/image.tar"` - Scans the supplied TAR image.
- `)` - Ends the PowerShell array.
- `docker @dockerArgs` - Runs Docker with all array arguments.

