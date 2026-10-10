#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
project_dir=$(cd -- "$script_dir/.." && pwd)
log_dir="$project_dir/logs"
log_file="$log_dir/application.log"

mkdir -p -- "$log_dir"
cat > "$log_file" <<'LOG'
2026-10-11T09:00:00+06:00 INFO Application started
2026-10-11T09:00:02+06:00 INFO Configuration loaded from config/app.conf
2026-10-11T09:00:04+06:00 WARNING Cache directory is not configured
2026-10-11T09:00:06+06:00 INFO Database connection established
2026-10-11T09:00:08+06:00 ERROR Request 1042 failed validation
2026-10-11T09:00:10+06:00 INFO Health check completed successfully
2026-10-11T09:00:12+06:00 WARNING Memory usage reached 75 percent
2026-10-11T09:00:14+06:00 ERROR Database query timed out
2026-10-11T09:00:16+06:00 INFO Database connection recovered
2026-10-11T09:00:18+06:00 INFO User session closed
2026-10-11T09:00:20+06:00 ERROR Background job failed after retry
2026-10-11T09:00:22+06:00 INFO Application stopped gracefully
LOG

printf 'Generated %s\n' "$log_file"
