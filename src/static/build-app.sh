#!/bin/bash

echo "Dropping current files..."

rm ./dist -rf

echo "Compiling the new!"

cd ./admin && npm install && npm run build && cd ..
cd ./client && npm install && npm run build && cd ..

echo "Done!"
