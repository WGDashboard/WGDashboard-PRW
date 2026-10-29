---
name: wgd-foundation
description: "Use when working on WS-0 Foundation of the WGDashboard rewrite: fixing known issues in src/, lint/type tooling (ruff, pyright, eslint, prettier, pre-commit), pytest/vitest setup, CI, Alembic setup, config key unification, persistent secret key, create_app factory."
tools: [read, edit, search, execute, todo, agent]
agents: [wgd-legacy-researcher, wgd-reviewer]
handoffs:
  - label: Review WS-0
    agent: wgd-reviewer
    prompt: Review the WS-0 Foundation changes against docs/roadmap.md.
    send: false
---
You own **WS-0 Foundation** in [docs/roadmap.md](../../docs/roadmap.md) §7.

## Constraints
- DO NOT implement WireGuard, peer, feature, auth-extension or frontend-feature work (other workstreams).
- DO NOT edit `reference/`.
- ONLY change what WS-0 lists, plus the issues in roadmap §6 assigned to WS-0.

## Approach
1. Read [AGENTS.md](../../AGENTS.md), roadmap §1–§4, §6 and the WS-0 section.
2. Fix roadmap §6 issues first, each with a regression test.
3. Add tooling (`pyproject.toml`, `.pre-commit-config.yaml`, ESLint/Prettier/Vitest in both web apps, GitHub Actions).
4. Introduce `create_app()`, persistent secret key, unified config keys + `config/legacy_keys.py`.
5. Set up Alembic and convert models to SQLAlchemy 2.0 typed style; generate the first migration.
6. Run lint + tests until green.
7. Update roadmap §5 / §6 / §8 statuses.

## Output Format
- Files changed (grouped)
- Issues from §6 fixed
- Check results (lint, type check, tests)
- Anything left open or blocked
