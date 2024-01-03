#bin/bash

mkdir ./server/node
mkdir ./server/node/index
mkdir ./server/node/extracted_texts
mkdir ./server/node/files

touch ./client/.env
echo "VITE_API_DOMAIN=http://localhost:8000" >> ./client/.env