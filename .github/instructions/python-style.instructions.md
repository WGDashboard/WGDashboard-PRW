---
description: "Use when writing or editing Python in the WGDashboard rewrite: readability-first coding style, naming, typing, logging, error handling, subprocess and SQLAlchemy rules."
applyTo: "src/**/*.py, tests/**/*.py, tools/**/*.py"
---
# Python style – readability first

The legacy code (`reference/`) is compact and dense. The rewrite deliberately is not.

## Rules

1. No `lambda`, `map()` or `filter()`. Use `for` loops, or a single-level comprehension with at most one simple `if`.
2. No nested ternaries. A ternary must fit on one short line.
3. One action per line. Store intermediate results in descriptively named variables instead of chaining calls.
4. Return early instead of nesting `if/else`. Max ~3 indentation levels inside a function body.
5. Descriptive names: `peer`, `interface_name`, `allowed_ips` – never `p`, `x`, `ca`, `iph`.
6. Type hints on every parameter and return value.
7. Functions return `tuple[bool, value]` to signal success (as in `src/modules/config/config.py`). Do not mix with raising for control flow.
8. Utility functions ALWAYS log at DEBUG. Services log INFO on state changes and ERROR on failure. Use `import logging as log`.
9. Functions ≲ 50 lines, files ≲ 400 lines. Split by responsibility.
10. Enums or module constants instead of magic strings (`PeerStatus`, `Protocol`, `JobAction`).
11. Subprocess: list arguments only, never `shell=True`, always a `timeout`, only inside `src/modules/wireguard/cli.py`.
12. SQLAlchemy 2.0 typed models (`Mapped[...]`, `mapped_column`). No SQL string formatting.
13. Request bodies are validated with pydantic models; respond with `make_resp_obj(status, message, data, http_code)`.
14. Keep existing conventions: `#!/bin/env python3` header, snake_case, `'''one-line docstrings'''`.

## Example

Legacy:
```python
"ConnectedPeers": len(list(filter(lambda x: x.status == "running", self.Peers))),
```

Rewrite:
```python
connected_peer_count = 0

for peer in peers:
    if peer.status == PeerStatus.RUNNING:
        connected_peer_count += 1
```

Helper style:
```python
def find_available_addresses(network: ipaddress.IPv4Network, used_addresses: set[str], limit: int) -> list[str]:
    '''Return up to `limit` host addresses in `network` that are not used yet.'''
    log.debug(f"searching available addresses in {network} (limit {limit})")

    available_addresses: list[str] = []

    for host in network.hosts():
        address = str(host)

        if address in used_addresses:
            continue

        available_addresses.append(address)

        if len(available_addresses) >= limit:
            break

    log.debug(f"found {len(available_addresses)} available addresses")
    return available_addresses
```
