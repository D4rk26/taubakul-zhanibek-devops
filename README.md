# taubakul_zhanibek

University DevOps laboratory project for practicing Linux and Git workflows in a reproducible Ubuntu environment.

## Student information

- Name: Zhanibek
- Surname: Taubakul
- Group: IT2-2302
- Student ID: 37650
- Course: DevOps

## Environment

- Host: macOS on Apple Silicon
- Linux environment: Ubuntu 24.04 ARM64 in Docker Desktop
- Reusable container: `taubakul-zhanibek-linux`
- Host project path: `~/devops/taubakul_zhanibek`
- Container project path: `/workspace/taubakul_zhanibek`

The project directory is bind-mounted, so its files persist when the container stops.

## Project structure

```text
.
├── Taubakul_Zhanibek_info.txt
├── app/
├── backup/                       # local and ignored by Git
├── config/
│   └── app.conf
├── logs/
│   └── application.log          # generated locally and ignored by Git
├── private.txt
├── public.txt
└── scripts/
    ├── Taubakul_Zhanibek_system.sh
    └── generate_application_log.sh
```

## Start the existing Ubuntu container

```bash
docker start taubakul-zhanibek-linux
docker exec --user student \
  --workdir /workspace/taubakul_zhanibek \
  taubakul-zhanibek-linux uname -m
```

The expected architecture is `aarch64`. This repository does not contain a Dockerfile or Compose configuration; those belong to a later laboratory phase.

## Run the system information script

```bash
docker exec --user student \
  --workdir /workspace/taubakul_zhanibek \
  taubakul-zhanibek-linux \
  ./scripts/Taubakul_Zhanibek_system.sh
```

The reported operating system, hostname, processes, memory, and disk view belong to the Ubuntu container or Docker VM/cgroup, not directly to macOS.

## Recreate and verify Linux Tasks 1–5

Recreate the ignored application log:

```bash
docker exec --user student \
  --workdir /workspace/taubakul_zhanibek \
  taubakul-zhanibek-linux \
  ./scripts/generate_application_log.sh
```

Run the Phase 2 verification scripts stored outside the repository:

```bash
docker exec --user student \
  --workdir /workspace/taubakul_zhanibek \
  taubakul-zhanibek-linux \
  bash /evidence/phase2/task1_verify.sh

docker exec --user student \
  --workdir /workspace/taubakul_zhanibek \
  taubakul-zhanibek-linux \
  bash /evidence/phase2/task2_verify.sh

docker exec --user student \
  --workdir /workspace/taubakul_zhanibek \
  taubakul-zhanibek-linux \
  bash /evidence/phase2/task4_verify.sh
```

Process evidence uses `ps`, `ps aux`, and non-interactive `top -b -n 1`. Permission access behavior is verified on the container's native Linux filesystem because Docker Desktop bind mounts expose mode bits but do not reliably enforce ordinary Linux access checks.

## Git workflow

- `main` is the integrated project branch.
- `development` is used for isolated, meaningful changes before merge.
- Commits group related changes and use descriptive conventional messages.
- Generated logs, backups, environment files, credentials, and editor artifacts are excluded through `.gitignore`.
- Force pushes and history rewriting are not part of this laboratory workflow.

The GitHub repository for Task 10 is `https://github.com/D4rk26/taubakul-zhanibek-devops`.

## Docker application

The Docker image uses Ubuntu 24.04 and Python's standard library. It runs as the non-root user `10001:10001`, exposes TCP port 8080, and includes an HTTP health check.

Build and inspect the image:

```bash
docker build -t taubakul-zhanibek-devops .
docker images taubakul-zhanibek-devops
docker image inspect taubakul-zhanibek-devops:latest
```

Run the personalized application on the loopback interface:

```bash
docker run -d \
  --name taubakul-zhanibek-container \
  -p 127.0.0.1:8080:8080 \
  -e STUDENT_NAME=Zhanibek \
  -e STUDENT_SURNAME=Taubakul \
  -e STUDENT_GROUP=IT2-2302 \
  -e STUDENT_ID=37650 \
  taubakul-zhanibek-devops

curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/health
docker ps
docker ps -a
```

The four `STUDENT_*` variables are read when the application starts. Environment variables separate runtime configuration from the image and make the same image reusable. Non-sensitive defaults are provided for this laboratory, but passwords, API tokens, and other secrets must never be hard-coded into an image or committed to Git.

Container lifecycle commands:

```bash
docker logs taubakul-zhanibek-container
docker exec taubakul-zhanibek-container id
docker stop taubakul-zhanibek-container
docker start taubakul-zhanibek-container
docker stop taubakul-zhanibek-container
docker rm taubakul-zhanibek-container
```

A Docker image is an immutable template containing the filesystem and runtime configuration. A container is a runtime instance of that image with its own process and lifecycle state.

## Docker Compose

Validate and start the service:

```bash
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs
curl http://127.0.0.1:8080/
docker compose down
```

Compose records the build, environment, port, health, and security configuration declaratively, so the service can be started consistently without repeating a long `docker run` command. The service binds only to `127.0.0.1`, uses a read-only root filesystem, drops Linux capabilities, and enables `no-new-privileges`.

The application is stateless, and Tasks 11–15 do not require persistent application data, so no Docker volume or host bind mount is added. Compose creates and removes its project-scoped default network automatically; no custom network is required.

## Jenkins CI/CD

The Jenkins Pipeline Job is named `Taubakul_Zhanibek_DevOps`. Jenkins runs locally on `127.0.0.1:8081` and loads this repository's root-level `Jenkinsfile` from the private GitHub repository with a dedicated read-only deploy key.

The Declarative Pipeline executes these required stages in order:

1. `Checkout` retrieves the selected Git commit from GitHub and records its SHA.
2. `Build` validates Python and Bash syntax, the Compose model, and student metadata.
3. `Test` runs the six application unit tests and prints the required student variables.
4. `Docker Build` creates an ARM64 image tagged with the Jenkins build number and Git SHA.
5. `Docker Run` starts a uniquely named non-root, read-only container and verifies health, successful HTTP output, a negative HTTP response, labels, logs, and runtime security settings.

The temporary CI container does not publish a host port, avoiding a conflict with Jenkins and the Compose development port. It is removed after evidence is emitted, while the traceable CI image remains available for inspection. Jenkins credentials and private deploy keys are stored outside this repository and are never passed to the application Pipeline environment.

The complete Linux → Git → GitHub → Jenkins → Docker integration and the eight Task 21 defense questions are documented in [Integrated DevOps Workflow](docs/INTEGRATED_DEVOPS_WORKFLOW.md).
