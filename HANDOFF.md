# HANDOFF.md — status antar mesin

Diperbarui: 2026-10-16 (Box ini)

## Mesin

| Mesin | Peran | Status |
|---|---|---|
| Windows 11 (box ini) | development, build tools, AI agent, OpenCode specialist | aktif |
| Kali Linux (T14s G1) | eksekusi aktif, pentest, pwn | aktif |
| Tab Sekolah | build tools/bypass/payload | kamu |
| Tab Rumah (tablet ini) | analisa, OSINT, source-code review | aktif |

## Konsep

Repo ini **parallel** dengan `Ptoolsdexeroid` — struktur & pola sama, bedanya:

| | Ptoolsdexeroid | Windev Specialist |
|---|---|---|
| Fokus | Pentest, OSINT, CTF, bypass | OpenCode Windows development |
| Platform | Linux-first | Windows-first |
| Audience | Red team | Developer + AI agent |
| Kit pattern | `kits/<name>/` + tests + README | `tools/<category>/<name>/` + tests |

## Struktur Windev Specialist

```
tools/
  recon/       — network & system recon (Windows)
  web/         — web development helpers (Windows)
  sysadmin/    — Windows administration & automation
  security/    — Windows security & hardening
  dev/         — OpenCode AI agent utilities
configs/       — config templates
tests/         — E2E tests
```

## Aturan Repo

1. **Credentials = env var only.** Never hardcode.
2. **Output kerja jangan di-commit.**
3. **Redact credentials** in any output (`<REDACTED>`).
4. **Consistent naming** — `tool_name.py` + `README.md` + `tests.py`.

## Changelog

- **2026-10-16** — repo dibuat, struktur awal.
- **2026-10-17** (Box ini, Windows 10) — 3 tool inti: `env_report`
  (sysadmin), `jsonc_check` + `ps51_lint` (dev); `tests/run_all.py` gate;
  19/19 tes lulus. ps51_lint diuji ke nyata: 28 file .ps1 paket 09-MIGRASI
  = 0 temuan.
