#!/bin/bash

echo "=== STAGED DIFF ==="
git diff --cached

echo "=== UNSTAGED DIFF ==="
git diff

echo "=== FILE LIST ==="
git status --porcelain
