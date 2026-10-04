
# EXPOSE the Streamlit port

Dockerfile:

```dockerfile
EXPOSE 8501
```

Interactively:

There is **no equivalent command inside the current walkthrough container**. `EXPOSE` adds information to the image. It does not open or publish a port.

For **development and production**, this line documents that the application is expected to use container port `8501`. The actual host connection is created later with `docker run -p ...`.

* `EXPOSE` → documents a network port that the container application uses. In the image metadata. See it with: `docker inspect <image-name>`
* `8501` → the container port that Streamlit will use.
* `EXPOSE 8501` does **not** publish port `8501` to the host.
* `docker run -p ...` → creates the host-to-container port mapping when the container starts.


`EXPOSE 8501` is **not required** for Docker port mapping.

Your container will still work with:

```text
-p 127.0.0.1:8501:8501
```

even if `EXPOSE 8501` is absent.

Keep it because it documents that the application uses container port `8501`. It is useful, but optional.