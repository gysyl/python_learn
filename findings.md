# Findings & Knowledge Base

## Technical Discoveries

### 1. `uv` Migration (2026-01-21)
- **Problem**: `uv` handles `sys.path` differently than standard `venv` when running pytest, causing `ModuleNotFoundError` for top-level packages in nested test directories.
- **Solution**: Configure `PYTHONPATH` in `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  pythonpath = ["."]
  ```
- **Key Commands**:
  - `uv sync`: Sync environment with lock file.
  - `uv add <package>`: Add dependency.
  - `uv run <command>`: Run command in virtual environment without explicit activation.

### 2. WSL Indexing Issues (2026-01-21)
- **Problem**: Trae/VS Code workspace indexing fails or times out in WSL.
- **Root Cause**: `.venv` directory contains thousands of small files, choking the file watcher.
- **Solution**: Move `.venv` outside the workspace or ensure it's in `.gitignore` (though file watcher might still scan it). *Current solution: Migration to `uv` also helps by centralizing cache, though local `.venv` still exists.*

## Project Structure
- **`web/blog_minimal`**: A standalone static site (HTML/CSS/JS) demonstrating minimalist design.
- **`.claude/skills`**: Custom skills directory for Claude Code.
