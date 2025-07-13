zerotier-gw-controller/docs/progress.md
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

---

## Development Workflow

**Key Process:**
- **Script-first iteration:** Develop and test the core controller script (`controller.py`) before packaging.
- **Rapid bugfix cycle:** Test on `phoney`, fix bugs, push changes.
- **Packaging after script works:** Only package once basic functionality is proven.
- **Automated install/config:** Use Ansible playbooks for install and config; avoid manual edits.

---

## Next Steps

1. **Create README.md** with project overview and quick start.
2. **Stub out core Python files**: `controller.py`, `cli.py`, `__init__.py`.
3. **Add example config file**: `debian/config.yaml.example`.
4. **Write initial test stubs** in `tests/`.
5. **Draft Ansible playbook placeholder** for future automation.
6. **Begin core logic implementation**: health check, failover, route update.

---

## Open Questions / Decisions

- **Ansible Playbook:** Where should playbooks live? (`ansible/` or `scripts/ansible/`)
- **Config reload:** Should the controller support live config reload, or require restart?
- **Testing strategy:** How to best mock ZeroTier API and ping for local dev?

---

## Issues & Blockers

_None at this time._

---

## Change Log

- **2024-06-10:** Project structure created, progress log started.

---

## How to Use This Doc

- Update after each major change, bugfix, or decision.
- Use for handoff between threads or contributors.
- Summarize current status and next steps at the top.

---