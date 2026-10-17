# Windev Specialist

OpenCode Windows specialist development toolkit.
Dibuat 2026-10-16.

## Konsep

Parallel dengan `Ptoolsdexeroid` — struktur & pola sama, fokus ke **OpenCode Windows development**.

| | Ptoolsdexeroid | Windev Specialist |
|---|---|---|
| Fokus | Pentest, OSINT, CTF, bypass | OpenCode Windows development |
| Platform | Linux-first | Windows-first |
| Audience | Red team | Developer + AI agent |

## Struktur

```
tools/
  recon/       — network & system recon (Windows)
  web/         — web development helpers (Windows)
  sysadmin/    — Windows administration & automation
    env_report/   — snapshot OS/versi tool/disk (4 tes)
  security/    — Windows security & hardening
  dev/         — OpenCode AI agent utilities
    jsonc_check/  — validasi config JSONC opencode.json (8 tes)
    ps51_lint/    — deteksi sintaks PS7-only di file .ps1 (7 tes)
configs/       — config templates
tests/run_all.py — gate: jalankan semua tests.py
HANDOFF.md     — status antar mesin
```

Jalankan semua tes: `python tests/run_all.py` (exit 0 hanya kalau semua lulus).

## Aturan Repo

1. **Credentials = env var only.** Never hardcode in config or script.
2. **Output kerja jangan di-commit** — itu artifact, bukan source.
3. **Read-only on target data** until operator confirms a change.
4. **Redact real credentials** in any output (`<REDACTED>`).

## Kit Pattern (sama seperti Ptoolsdexeroid)

Setiap tool punya:
- `tool_name.py` — script utama
- `README.md` — dokumentasi + cara pakai
- `tests.py` — E2E tests

## Changelog

- **2026-10-16** — repo dibuat.
- **2026-10-17** — 3 tool inti pertama (`f8613d0`): `sysadmin/env_report`,
  `dev/jsonc_check`, `dev/ps51_lint` — 19 tes lulus (`tests/run_all.py`).
