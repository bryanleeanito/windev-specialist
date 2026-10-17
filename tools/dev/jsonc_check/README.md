# jsonc_check — validasi config JSONC (komentar + trailing comma)

Validasi `opencode.json` dan config JSONC lain: komentar `//`/`/* */` dan
trailing comma ditolerir, tapi error JSON ASLI tetap ketahuan dengan **nomor
baris/kolom akurat** (komentar di-blank jadi spasi, bukan dihapus — posisi
teks tidak bergeser).

```bash
python jsonc_check.py "%USERPROFILE%\.config\opencode\opencode.json"
python jsonc_check.py --json a.json b.json
```

Keluaran:

```
[OK]   config-valid.json
[FAIL] config-rusak.json — baris 3, kolom 9: Expecting value
```

Exit code: `0` semua valid · `1` ada invalid · file `utf-8-sig` (BOM aman).

Kenapa perlu: bug nyata 16 Okt 2026 — config `plugins` jadi file karena
install rusak; validasi JSONC sebelum/jalankan ulang installer mencegah
config mati diam-diam.

Tes: `python tests.py` (8 tes, termasuk smoke test config live kalau ada).
