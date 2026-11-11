#!/bin/sh
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../../.." && pwd)
if [ ! -x "$ROOT/.agentlab/venv/bin/python" ]; then
  printf '%s\n' 'Önce AgentLab kurulumunu çalıştırın. / Run AgentLab setup first.'
  exit 1
fi
exec "$ROOT/.agentlab/venv/bin/python" "$HERE/app.py"
