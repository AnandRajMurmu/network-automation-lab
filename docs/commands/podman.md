# PODMAN COMMANDS

#### 1. Check Podman Images

```bash
podman images
```

Lists downloaded container images available locally.

#### 2. List Pods

```bash
podman pod ps
```

Lists pods (groups of containers), their status, and the number of containers in each pod.

#### 3. List All Containers

```bash
podman ps -a
```

Lists all containers, including running, stopped, and created-but-not-running containers. Without -a, lists only running containers.

#### 4. Create a Pod

```bash
podman pod create --name nlab-app -p 127.0.0.1:8080:80
```

Creates a pod named nlab-app and maps host port 8080 to container port 80, accessible only from the local machine.

#### 5. Run a Container Inside a Pod

```bash
podman run -d --name nlab-nginx --pod nlab-app docker.io/library/nginx:alpine
```

Creates and starts an Nginx container inside nlab-app.
run: Creates and starts a container.
-d: Runs it in the background.
--name: Assigns a container name.
--pod: Places the container in an existing pod.
nginx:alpine: Specifies the Nginx image with the Alpine Linux base.

#### 6. Remove a Container

```bash
podman rm -f nlab-nginx
```

Force-removes the named container, stopping it first if necessary. Does not intentionally remove its pod.

#### 7. Remove All Containers

```bash
podman rm -f -a
```

Force-removes all containers, including pod infrastructure containers. This can also cause the pods to disappear, so do not use it when you want to preserve your pods.

#### 8. View Container Logs

```bash
podman logs --tail 20 nlab-nginx
```

Displays the most recent 20 log lines from the Nginx container.

#### 9. Inspect a Pod

```bash
podman pod inspect nlab-app
```

Displays detailed information about the specified pod, including its configuration and networking.

#### 10. List Containers in a Specific Pod

```bash
podman ps -a --filter pod=nlab-app
```

Lists all containers belonging to the `nlab-app` pod, including running, stopped, and created-but-not-running containers. This helps you check the status of Nginx, Python, PostgreSQL, and the pod's infrastructure container without listing containers from other pods.

#### 11. List Containers by Name

```bash
podman ps -a --format "{{.Names}}"
```

Lists the names of all containers, including running, stopped, and created-but-not-running containers.

To display container names along with their status:

```bash
podman ps -a --format "table {{.Names}}\t{{.Status}}"
```

To display names and status for containers inside a specific pod, such as `nlab-app`:

```bash
podman ps -a --filter pod=nlab-app --format "table {{.Names}}\t{{.Status}}"
```

#### 12. Execute a Command Inside a Container

```bash
podman exec nlab-api pip install fastapi uvicorn
```

Runs a command inside an existing, running container without creating a new container. In this example, it installs FastAPI and Uvicorn inside `nlab-api`.

**Example 1 — Open an interactive shell**

```bash
podman exec -it nlab-nginx sh
```

Opens a shell inside the running Nginx container so you can execute commands interactively. Type `exit` to leave the container shell.

**Example 2 — Check the Python version**

```bash
podman exec nlab-api python --version
```

Executes `python --version` inside the running `nlab-api` container and displays the installed Python version.

#### 13. Build a Container Image

```bash
podman build -t localhost/nlab-api:0.1.0 -f app/backend/Dockerfile app/backend
```

Builds a custom container image from a `Dockerfile` and the specified build context.

**Command breakdown:**
- `podman build` — builds an image.
- `-t localhost/nlab-api:0.1.0` — assigns the image name and tag (`0.1.0` is the version).
- `-f app/backend/Dockerfile` — specifies the Dockerfile to use.
- `app/backend` — sets the build context, the directory whose files are available to the build.

**List available images:**

```bash
podman images
```

Displays locally available images, including their repository, tag, ID, and size.

**Note:** An image is a reusable template. You can create multiple containers from the same image using `podman run`.

## Project Commands

### Pull Images
```bash
podman pull alpine:latest
```

```bash
podman pull codeberg.org/forgejo/forgejo:16
```

```bash
podman pull data.forgejo.org/forgejo/runner:13
```

```bash
podman pull docker.io/library/nginx:alpine
```

```bash
podman pull docker.io/library/python:3.12-slim
```

```bash
podman pull docker.io/library/postgres:17-alpine
```

### Create Pods
```bash
podman pod create \
  --name nlab-devops \
  -p 127.0.0.1:3000:3000 \
  -p 127.0.0.1:2222:22
```

```bash
podman pod create \
  --name nlab-app \
  -p 127.0.0.1:8080:80
```

```bash
podman pod create \
  --name nlab-network
```

### Create Containers

```bash
podman run -d \
  --name nlab-nginx \
  --pod nlab-app \
  docker.io/library/nginx:alpine
```

```bash
read -rsp "Enter PostgreSQL password: " PG_PASSWORD
echo
podman run -d \
  --name nlab-postgres \
  --pod nlab-app \
  -e POSTGRES_USER=nlab \
  -e POSTGRES_PASSWORD="$PG_PASSWORD" \
  -e POSTGRES_DB=networklab \
  -v "$PWD/data/postgres:/var/lib/postgresql/data" \
  docker.io/library/postgres:17-alpine
unset PG_PASSWORD
```

```bash
podman run -d \
  --name nlab-api \
  --pod nlab-app \
  docker.io/library/python:3.12-slim \
  python -c "import time; print('Python backend container ready', flush=True); time.sleep(1000000)"
```

### Run Exec Commands

#### Postgress:
```bash
podman exec -it nlab-postgres psql -U nlab -d networklab
```
