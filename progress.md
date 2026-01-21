# Progress Log

## 2026-01-21

### 1. Project Initialization & Setup
- **Action**: Created virtual environment manually using `python -m venv` (later replaced).
- **Action**: Synced with GitHub repository `gysyl/python_learn`.

### 2. Feature Implementation: Minimal Blog
- **Action**: Designed and implemented `web/blog_minimal/` with semantic HTML, CSS variables, and micro-interactions.
- **Outcome**: Created a production-ready static landing page.

### 3. Infrastructure: Migration to `uv`
- **Action**: Installed `uv` on WSL environment.
- **Action**: Generated `pyproject.toml` from `requirements.txt`.
- **Action**: Resolved `ModuleNotFoundError` in pytest by updating `pyproject.toml` configuration.
- **Action**: Created `scripts/bootstrap.sh` for one-click environment setup.
- **Outcome**: Successfully migrated dependency management to `uv`.

### 4. Workflow: Adopt `planning-with-files`
- **Action**: Initialized `task_plan.md`, `findings.md`, and `progress.md`.
- **Outcome**: Established persistent context for future tasks.
