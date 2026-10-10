# Integrated DevOps Workflow — Task 21

Student: Zhanibek Taubakul

Group: IT2-2302

Student ID: 37650

## Complete workflow

```text
Linux
  ↓
Create Project
  ↓
Git
  ↓
GitHub
  ↓
Jenkins
  ↓
Build
  ↓
Test
  ↓
Docker Build
  ↓
Docker Run
  ↓
SUCCESS
```

This repository implements the chain as one traceable process:

1. Ubuntu 24.04 ARM64 provides the Linux environment used to create and verify the project files, Bash script, logs, permissions, and processes.
2. Git records each meaningful project change in the local repository.
3. GitHub stores the private remote repository and its `main` branch.
4. Jenkins Job `Taubakul_Zhanibek_DevOps` obtains the root `Jenkinsfile` and source from GitHub with a repository-scoped read-only SSH deploy key.
5. The Pipeline validates the project in Build and executes the real Python unit tests in Test.
6. Docker Build creates an ARM64 image labelled with the exact checked-out Git commit.
7. Docker Run starts a uniquely named container and verifies health, HTTP responses, student environment variables, non-root execution, and read-only filesystem behavior.
8. Jenkins reports SUCCESS only when every mandatory command returns successfully. The Console Output and image revision label connect the result back to the exact GitHub commit.

## Why do we use Linux?

Linux provides the target operating environment for the laboratory and for the Docker image. It supplies standard tools such as Bash, `find`, `grep`, `chmod`, `ps`, and `top`, making file, permission, process, and automation behavior reproducible. In this project the reusable container `taubakul-zhanibek-linux` runs Ubuntu 24.04 ARM64 and bind-mounts the project so its files persist on macOS.

## Why do we use Git?

Git records changes as identifiable commits, keeps a reviewable history, and supports isolated development branches and controlled merges. It allows a defect and its correction to remain visible instead of overwriting history. The final commit SHA is also the traceability identifier used by Jenkins and Docker.

Useful verification commands:

```bash
git status --short --branch
git log --oneline --graph --all --decorate
git show --stat HEAD
```

## Why do we use GitHub?

GitHub is the remote source of truth shared by Git and Jenkins. It preserves the synchronized repository outside the local working tree and gives Jenkins a stable SCM URL and branch. The repository remains private, so Jenkins uses a dedicated read-only deploy key rather than a personal write token.

## Why does Jenkins need GitHub?

Jenkins needs GitHub to retrieve the committed `Jenkinsfile` and the exact source revision that must be built. The Job is configured as Pipeline from SCM for:

```text
git@github.com:D4rk26/taubakul-zhanibek-devops.git
branch: */main
script path: Jenkinsfile
```

Checkout records the full SHA in Console Output. This proves that Jenkins tested repository content rather than unrelated files from an interactive shell.

## Why does Jenkins build the Docker image?

Building the image in Jenkins makes packaging part of the same automated, repeatable quality gate as source validation and tests. Jenkins stops if `docker build` fails. A successful image is checked for ARM64 architecture, the non-root `10001:10001` user, healthcheck, and an `org.opencontainers.image.revision` label equal to the checked-out Git SHA.

## What is the difference between a Docker image and container?

A Docker image is an immutable template containing the application filesystem and runtime configuration. A container is a running or stopped instance created from that image, with its own process and state. This Pipeline retains the traceable CI image but removes the temporary CI container after its live behavior has been captured in Console Output.

## What happens when the Jenkins Pipeline starts?

1. Jenkins allocates its local workspace and applies the timeout and non-concurrency policy.
2. Checkout deletes stale workspace content and retrieves `main` from the private GitHub repository.
3. Build verifies Python and Bash syntax, Docker Compose configuration, required files, and student metadata.
4. Test runs six Python unit tests, including validation failures, and prints the four required student variables.
5. Docker Build creates a uniquely tagged ARM64 image and verifies its metadata and commit label.
6. Docker Run creates a uniquely named secure container, waits for `healthy`, verifies `/`, `/health`, and HTTP 404 behavior, and captures the container state and logs.
7. Post actions stop and remove only that build's temporary CI container.
8. Jenkins returns `Finished: SUCCESS` only after every mandatory stage and cleanup succeeds.

## What happens if one Pipeline stage fails?

The failing command returns a non-zero exit code, the current stage becomes FAILURE, and later mandatory stages are skipped. Jenkins still runs the controlled post action so a temporary CI container cannot be left behind. The overall build ends with `Finished: FAILURE`; the failed build remains in history for diagnosis.

This behavior was demonstrated by Jenkins build #1: an incorrect student-file assertion failed in Build, Test/Docker stages were skipped, and Jenkins recorded FAILURE. After correcting the root cause in commit `90f85f3`, builds #2 and #3 completed successfully. No error was hidden with `|| true` or a forced exit code 0.

## Reproducing the integrated verification

Local source checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
docker compose config --quiet
git status --short --branch
```

Jenkins runs the complete workflow from the private GitHub `main` branch. Its Console Output must show the checkout SHA, all five required stages, six passing tests, student information, image/container evidence, and the final line `Finished: SUCCESS`.

The checked-out Git SHA, GitHub `main` SHA, and Docker image revision label must all be identical.
