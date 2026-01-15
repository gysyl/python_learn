#!/bin/bash

MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
  echo "Error: commit message is empty"
  exit 1
fi

git add .
git commit -m "$MESSAGE"
git push
