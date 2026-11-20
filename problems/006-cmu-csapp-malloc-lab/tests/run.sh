#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
gcc -std=c11 -Wall -Wextra -o /tmp/csapp_malloc_test ../solution/malloc.c test_malloc.c
/tmp/csapp_malloc_test
