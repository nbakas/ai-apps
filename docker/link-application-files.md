# Link the application files

> The Dockerfile `COPY` is for **production, and Hugging Face Spaces**. It makes the application part of the image.

Dockerfile:

```dockerfile
COPY app.py *.so ./
```

* `COPY` -> copies files from the Docker build context into the image.
* `app.py *.so` -> copies only the application script and the compiled `.so` modules, nothing else.
* `./` -> current directory inside the image. Because `WORKDIR /app` is already set, this means `/app`. With more than one source, the destination must end with `/`.
* No `--chown` -> the files belong to `root`. `appuser` can read and run them, but cannot change or delete them. The application still runs as `appuser` because of `USER appuser`.

> Do not add `/app` to the `chown -R` of `appuser`. If `appuser` owns the `/app` directory, it can delete and replace the root-owned files inside it.

> The application writes only to the mounted `/app/my-projects` directory, not next to its code.

> Use `.dockerignore` to keep files such as `.git`, caches, secrets, and local user data out of the build context. `COPY` now copies only the named files, but `.dockerignore` also stops unnecessary files from being sent to the builder.

> `.dockerignore` affects only the Docker build context. It does not affect bind mounts or `docker cp`. You can still copy files into a running container with `docker cp` or mount them with `-v`.

> See attached `.dockerignore` for a recommended starting point. Add any additional files or directories that you do not want in the build context!