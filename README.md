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
