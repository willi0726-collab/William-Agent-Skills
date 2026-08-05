---
name: headroom
description: Use when installing, configuring, verifying, or using Headroom, the local token and context optimization tool, including headroom CLI commands, proxy, MCP server, memory, wrap codex, unwrap codex, perf, and compression workflows.
---

# Headroom

## Local Install

Headroom is installed in an isolated Python environment:

- CLI: `C:\Users\ZhuanZ\.codex\tools\headroom\Scripts\headroom.exe`
- Wrapper: `C:\Users\ZhuanZ\.codex\bin\headroom.cmd`
- Package: `headroom-ai==0.20.15` with `proxy,mcp` extras

Use the wrapper when it exists. Use the direct CLI path when PATH does not include `C:\Users\ZhuanZ\.codex\bin`.

## Safe Workflow

1. Start with read-only discovery:
   - `headroom --help`
   - `headroom --version`
   - `headroom perf --help`
   - `headroom proxy --help`
   - `headroom mcp --help`

2. Before changing Codex or agent behavior, explain exactly what will change and ask for confirmation. This includes:
   - `headroom wrap codex`
   - `headroom unwrap codex`
   - `headroom init ...`
   - persistent proxy, MCP, service, or startup integration changes

3. Prefer a reversible setup:
   - Capture current config paths before writes.
   - Use read-only checks first.
   - Keep proxy or service commands in foreground unless the user asks for a persistent service.

## Version Notes

The upstream repository is `https://github.com/headroomlabs-ai/headroom`. The public quick start points at `pip install "headroom-ai[all]"`, but this Windows machine has a verified local install of `0.20.15`.

Do not claim latest-version features unless `headroom --help` or the installed package confirms them. For example, this verified install does not expose every command mentioned by the latest README.

If updating:

- Prefer the isolated venv at `C:\Users\ZhuanZ\.codex\tools\headroom`.
- Check whether a Windows wheel exists before upgrading.
- If pip selects a source distribution, verify build dependencies before modifying the working install.
- If network downloads are unstable, use a reliable mirror and retries.

## Verification

For install or config work, verify with:

```powershell
& 'C:\Users\ZhuanZ\.codex\tools\headroom\Scripts\headroom.exe' --help
& 'C:\Users\ZhuanZ\.codex\tools\headroom\Scripts\headroom.exe' --version
& 'C:\Users\ZhuanZ\.codex\tools\headroom\Scripts\python.exe' -m pip show headroom-ai
```

If this local skill changes, also run:

```powershell
& 'C:\Users\ZhuanZ\AppData\Local\Programs\Python\Python312\python.exe' 'C:\Users\ZhuanZ\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'C:\Users\ZhuanZ\.codex\skills\headroom'
```
