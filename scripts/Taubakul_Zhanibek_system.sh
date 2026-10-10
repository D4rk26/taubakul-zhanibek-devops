#!/usr/bin/env bash
set -uo pipefail

if (( $# != 0 )); then
    printf 'Usage: %s\n' "$(basename "$0")" >&2
    exit 64
fi

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
project_dir=$(cd -- "$script_dir/.." && pwd)
info_file="$project_dir/Taubakul_Zhanibek_info.txt"

printf '%s\n' '=============================='
printf '%s\n' 'Student Information'
printf '%s\n\n' '=============================='
printf '%s\n' 'Name: Zhanibek'
printf '%s\n' 'Surname: Taubakul'
printf '%s\n' 'Group: IT2-2302'
printf '%s\n\n' 'Student ID: 37650'

printf '%s\n' '=============================='
printf '%s\n' 'System Information'
printf '%s\n\n' '=============================='
printf 'Username: %s\n' "$(whoami)"
printf 'Hostname: %s\n' "$(hostname)"
printf 'Current Date: %s\n' "$(date --iso-8601=seconds)"
if [[ -r /etc/os-release ]]; then
    . /etc/os-release
    printf 'Operating System: %s\n' "${PRETTY_NAME:-$(uname -s)}"
else
    printf 'Operating System: %s\n' "$(uname -srm)"
fi
printf '%s\n' 'Disk Usage:'
df -h "$project_dir"
printf '%s\n' 'Memory Usage:'
free -h

if [[ -f "$info_file" ]]; then
    printf '%s\n' 'Student information file exists.'
    exit 0
fi

printf '%s\n' 'Student information file does not exist.'
exit 1
