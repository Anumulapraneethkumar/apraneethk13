#!/bin/bash
set -e
echo "Compiling Java backend..."
mkdir -p bin
javac -d bin java_backend/*.java
echo "Compiled to bin/"
