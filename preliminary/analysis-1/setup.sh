#!/bin/bash
set -e

command -v docker >/dev/null || { echo "Docker required: https://docs.docker.com/engine/install/"; exit 1; }
command -v git >/dev/null || { echo "Git required"; exit 1; }

WORKDIR="/tmp/ip-demo-$$"
git clone --depth 1 https://github.com/Achxy/aurora-autopsy.git "$WORKDIR"
cd "$WORKDIR/preliminary/analysis-1"

docker compose up -d --build

IP=$(curl -4 -s ifconfig.me 2>/dev/null || echo "YOUR_SERVER_IP")
echo "Visit: http://$IP"
echo "Logs:  cd $WORKDIR/preliminary/analysis-1 && docker compose logs -f app"
