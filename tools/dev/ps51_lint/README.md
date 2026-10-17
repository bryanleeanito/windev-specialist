# ps51_lint — deteksi sintaks PS7 yang gagal di PowerShell 5.1

Windows 5.1 (default) tidak punya `&&`/`||` (pipeline chain), `??`
(null-coalescing), `?.` (null-conditional). Sintaks ini bikin script mati
dengan error aneh — deteksi sebelum run, bukan setelah gagal.

```bash
python ps51_lint.py script.ps1
python ps51_lint.py C:\path\ke\folder        # walk *.ps1 / *.psm1
python ps51_lint.py --json a.ps1 b\
```

Keluaran:

```
script.ps1:12:34 [&&] pipeline chain '&&' hanya di PS7 — pakai `cmd; if ($?) { ... }`
[hasil] 1 temuan di 1 file (0 path hilang)
```

- String (`"..."`/`'...'`), komentar (`#`, `<# #>`) di-skip → false positive minim.
- Exit code: `0` bersih · `1` ada temuan · `2` path tidak ditemukan.
- Solusi pengganti tercetak di tiap pesan temuan (gaya `cmd1; if ($?) { cmd2 }`).

Tes: `python tests.py` (7 tes).
