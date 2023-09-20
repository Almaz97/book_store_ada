#!/bin/sh

echo trying to start beat

set -o errexit
set -o pipefail
set -o nounset

celery -A core beat --loglevel=info
