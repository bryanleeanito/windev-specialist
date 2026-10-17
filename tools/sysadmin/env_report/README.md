# env_report — snapshot lingkungan Windows

Laporan cepat: OS, versi python/node/npm/git, disk per drive, jumlah PATH.
Read-only, stdlib only — aman dijalankan di mesin mana pun.

```bash
python env_report.py            # laporan teks
python env_report.py --json     # JSON buat agent/CI
```

Contoh output (teks):

```
hostname : DEVBOX
os       : Windows-10-10.0.19045-SP0
python   : 3.15.0
node     : v24.22.0
...
disk     :
  C:\   123.4 GB bebas (45.2%) dari 273.0 GB
  [!] D: sisa <10% — bersihkan space
```

- Exit 0 selama laporan bisa dibuat.
- Peringatan otomatis kalau drive sisa <10%.
- Jalur user tidak ditampilkan selain lewat PATH count — tidak ada kredensial.

Tes: `python tests.py` (4 tes).
