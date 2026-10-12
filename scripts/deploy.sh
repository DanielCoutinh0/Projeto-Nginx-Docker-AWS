#!/usr/bin/env bash

set -euo pipefail

VERSION=$(git rev-parse --short HEAD)

echo ">> Build da imagem (versão $VERSION)"
docker build --build-arg APP_VERSION="$VERSION" -t webapp:latest .

echo ">> Reiniciando o container"
docker rm -f webapp 2>/dev/null || true
docker run -d --name webapp --restart unless-stopped -p 127.0.0.1:3000:3000 webapp:latest

echo ">> Verificando se a aplicação respondeu"
for i in $(seq 1 10); do
  if curl --fail --silent http://127.0.0.1:3000/health > /dev/null; then
    echo ">> Deploy OK (versão $VERSION)"
    docker image prune -f > /dev/null
    exit 0
  fi
  sleep 2
done

echo "!! A aplicação não respondeu. Logs do container:"
docker logs webapp
exit 1
