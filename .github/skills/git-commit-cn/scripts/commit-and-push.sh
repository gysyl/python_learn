#!/bin/bash

MESSAGE="${1:-}"

if [ -z "$MESSAGE" ]; then
  echo "Error: commit message is empty"
  exit 1
fi

cd "$(git rev-parse --show-toplevel)" || exit 1

# Check if there are changes to commit
if ! git diff --cached --quiet; then
  # Stage all changes
  git add .
  
  # Commit with provided message
  if git commit -m "$MESSAGE"; then
    echo "✓ Commit successful: $MESSAGE"
  else
    echo "✗ Commit failed"
    exit 1
  fi
else
  echo "No staged changes to commit"
fi

# Push to remote
if git push; then
  echo "✓ Push successful"
else
  echo "✗ Push failed"
  exit 1
fi
