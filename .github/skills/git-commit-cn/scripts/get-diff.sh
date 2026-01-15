#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== STAGED DIFF ==="
git diff --cached

echo "=== UNSTAGED DIFF ==="
git diff

echo "=== FILE LIST ==="
git status --porcelain
