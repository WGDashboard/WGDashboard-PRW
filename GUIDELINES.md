# WGDashboard Coding Guidelines

## Rules

Follow the readability, typing, logging, SQLAlchemy, and layering conventions in
[docs/roadmap.md](docs/roadmap.md) §2.

- Utility functions must log at DEBUG; services log state changes at INFO and failures at ERROR.
- Code as verbose as possible and where reason allows it.