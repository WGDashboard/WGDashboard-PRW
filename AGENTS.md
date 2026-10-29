# WGDashboard Rewrite – Agent Rules

These rules apply to every agent and contributor working in this repository.

## Project

- `reference/` is the **legacy** WGDashboard. It is read-only: never edit, move or format anything in it.
- `src/` is the rewrite (Flask backend + `src/web/admin` and `src/web/client` Vue apps).
- [docs/roadmap.md](docs/roadmap.md) is the source of truth: architecture (§3), conventions (§4),
  endpoint mapping (§5), known issues (§6), workstreams (§7), parity checklist (§8),
  security requirements (§9) and open decisions (§10).
- Role agents live in [.github/agents/](.github/agents/). Coding style rules live in
  [.github/instructions/](.github/instructions/) and in [GUIDELINES.md](GUIDELINES.md).

## Always

1. Readability is the top priority. More lines of clear code beats fewer lines of clever code.
2. Re-implement legacy behaviour; never copy legacy code style.
3. Stay inside the scope of your workstream. If something outside it is broken, report it instead of fixing it.
4. Check a workstream's *Depends on* list in the roadmap before starting it.
5. Follow the **recommended default** of any decision in roadmap §10 that is still `open`.
6. Ship tests with every change (pytest for backend, Vitest for frontend).
7. Ship an Alembic migration with every schema change.
8. After implementing a route or feature, update its status in roadmap §5 and §8.

## Never

- Use `shell=True`, or call `wg`/`awg`/`wg-quick`/`awg-quick`/`ip`/`iptables` outside `src/modules/wireguard/cli.py`.
- Build SQL with string formatting.
- Log passwords, private keys, TOTP secrets, API keys or tokens.
- Add files to `reference/`.

## Layering

```
routes/*   -> parse + validate request (pydantic), call one service, return make_resp_obj
services   -> business logic
database/* -> ORM models and queries
wireguard/cli.py -> the only place that runs subprocesses
```
