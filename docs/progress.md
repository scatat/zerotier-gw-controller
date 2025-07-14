# ZeroTier Gateway Controller: Development Progress Log

This document tracks the ongoing development, decisions, issues, and next steps for the ZeroTier Gateway Controller project. It is intended to provide a clear snapshot of project status for easy context switching and onboarding.

---

## Project Initialization

**Date:** 2024-06-10  
**Status:** Repository bootstrapped, initial structure created.

### Actions Completed
- Created directory structure per specification:
  - `src/zerotier_gateway_controller/`
  - `tests/`
  - `debian/`
  - `docs/`
  - `.github/workflows/`
  - `scripts/`
- Added this progress log for ongoing tracking.
- Planning for README.md and initial stub files.
- Fixed all invalid first lines (path markers) in repo files.
- Updated workflow to use latest actions and correct YAML syntax.
- Ensured all steps use proper indentation and keys.
- Added debug step to locate .deb files after build.
- Fixed artifact upload to avoid forbidden relative paths.
- Moved .deb file into project directory for artifact upload.
- Migrated Python package metadata from setup.py to pyproject.toml.
- Fixed debian packaging to use pybuild and modern debhelper.

---

## Development Workflow

**Key Process:**
- **Script-first iteration:** Develop and test the core controller script (`controller.py`) before packaging.
- **Rapid bugfix cycle:** Test on `phoney`, fix bugs, push changes.
- **Packaging after script works:** Only package once basic functionality is proven.
- **Automated install/config:** Use Ansible playbooks for install and config; avoid manual edits.

---

## Next Steps

1. **Verify .deb artifact upload in CI** (now moved into project directory).
2. **Continue to iterate on controller logic and tests.**
3. **Feed updated progress doc into next thread for continuity.**
4. **Review and update documentation for packaging and workflow changes.**
5. **Monitor for any further warnings or errors in CI and address immediately.**

---

## Open Questions / Decisions

- **Ansible Playbook:** Where should playbooks live? (`ansible/` or `scripts/ansible/`)
- **Config reload:** Should the controller support live config reload, or require restart?
- **Testing strategy:** How to best mock ZeroTier API and ping for local dev?
- **Python packaging:** Should all metadata be managed in pyproject.toml only, or keep setup.py for legacy?
- **Artifact upload:** Is moving .deb into project root the best long-term solution, or should build script be updated?

---

## Issues & Blockers

- Setuptools/pyproject.toml warnings about metadata outside pyproject.toml (fixed by migration).
- Artifact upload error: relative paths forbidden (fixed by moving .deb into project directory).
- YAML syntax errors due to indentation, missing keys, or invalid first lines (fixed).
- Debhelper/pybuild packaging errors (fixed by updating debian/rules and workflow).

---

## Change Log

- **2024-06-10:** Project structure created, progress log started.
- **2024-06-11:** Invalid first lines removed from all files. Workflow YAML and packaging issues fixed. Python metadata migrated to pyproject.toml. Artifact upload and debug steps corrected.

---

## How to Use This Doc

- Update after each major change, bugfix, or decision.
- Use for handoff between threads or contributors.
- Summarize current status and next steps at the top.

---