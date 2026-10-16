# Windev Specialist

Windows specialist development toolkit for OpenCode AI Agent.
Dibuat 2026-10-16.

## Peran

| Mesin | Peran |
|---|---|
| Windows 11 (box ini) | development, build tools, AI agent |
| Kali Linux (T14s G1) | eksekusi aktif, pentest, pwn |

## Struktur

```
tools/           — PowerShell & Python scripts
  recon/         — network & system recon
  web/           — web development helpers
  sysadmin/      — Windows administration
  security/      — Windows security & hardening
  dev/           — development utilities
configs/         — config templates
tests/           — E2E tests
```

## Aturan repo

1. **Credentials = env var only.** Never hardcode in config or script.
2. **Output kerja jangan di-commit** — itu artifact, bukan source.
3. **Read-only on target data** until operator confirms a change.
4. **Redact real credentials** in any output (`<REDACTED>`).

## Changelog

- **2026-10-16** — repo dibuat.
