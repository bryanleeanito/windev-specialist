#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps51_lint.py — deteksi sintaks PowerShell 7 yang GAGAL di PowerShell 5.1.

Mesin ini (dan kebanyakan Windows) pakai PowerShell 5.1 — sintaks PS7 bikin
script mati dengan error aneh. Cek dulu sebelum run:

    python ps51_lint.py script.ps1
    python ps51_lint.py C:\\path\\ke\\folder        # walk *.ps1/*.psm1
    python ps51_lint.py --json a.ps1 b\\            # output JSON

Aturan:
  && / ||   pipeline chain (PS7)  -> pakai `cmd; if ($?) { ... }`
  ?? / ?.   null-coalescing (PS7) -> pakai `if ($null -ne $x) { ... }`

String dan komentar di-skip dulu supaya false positive minim.
Exit 0 = bersih, 1 = ada temuan, 2 = file tidak ada.
"""
import argparse
import json
import os
import re
import sys

ATURAN = (
    ("&&", "pipeline chain '&&' hanya di PS7 — pakai `cmd; if ($?) { ... }`"),
    ("||", "pipeline chain '||' hanya di PS7 — pakai `cmd; if (-not $?) { ... }`"),
    ("??", "null-coalescing '??' hanya di PS7 — pakai `if ($null -ne $x) { $x }`"),
    ("?.", "null-conditional '?.' hanya di PS7 — pakai `if ($null -ne $x) { $x.prop }`"),
)


def blank_string_komentar(s):
    """Kosongkan isi string & komentar PowerShell (baris tetap stabil)."""
    out = list(s)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in "\"'":
            tutup = c
            i += 1
            while i < n:
                if s[i] == "\n":
                    break  # string satu baris; lintas baris = bukan string
                if tutup == "'" and s[i] == "'":       # '' = escape di PS
                    if i + 1 < n and s[i + 1] == "'":
                        out[i] = out[i + 1] = " "
                        i += 2
                        continue
                    break
                if tutup == '"' and s[i] == "`":       # backtick escape
                    out[i] = out[i + 1] = " "
                    i += 2
                    continue
                if tutup == '"' and s[i] == '"':
                    break
                out[i] = " "                           # isi string dikosongkan
                i += 1
        elif c == "#" and (i == 0 or s[i - 1] != "<"):
            while i < n and s[i] != "\n":
                out[i] = " "
                i += 1
            continue
        elif c == "<" and i + 1 < n and s[i + 1] == "#":
            out[i] = out[i + 1] = " "
            i += 2
            while i < n and not (s[i] == "#" and i + 1 < n and s[i + 1] == ">"):
                if s[i] != "\n":
                    out[i] = " "
                i += 1
            if i < n:
                out[i] = out[i + 1] = " "
                i += 1
        i += 1
    return "".join(out)


def cari(teks):
    """Return daftar {baris, kolom, aturan, pesan} dari satu isi file."""
    bersih = blank_string_komentar(teks)
    temuan = []
    for pola, nama, pesan in (
            (r"&&", "&&", ATURAN[0][1]),
            (r"\|\|", "||", ATURAN[1][1]),
            (r"\?\?", "??", ATURAN[2][1]),
            (r"\?\.", "?.", ATURAN[3][1])):
        for m in re.finditer(pola, bersih):
            baris = bersih.count("\n", 0, m.start()) + 1
            awal_baris = bersih.rfind("\n", 0, m.start()) + 1
            temuan.append({"baris": baris,
                           "kolom": m.start() - awal_baris + 1,
                           "aturan": nama, "pesan": pesan})
    temuan.sort(key=lambda t: (t["baris"], t["kolom"]))
    return temuan


def kumpul_file(paths):
    file, hilang = [], []
    for p in paths:
        if os.path.isfile(p):
            file.append(p)
        elif os.path.isdir(p):
            for akar, _, nama in os.walk(p):
                for n in nama:
                    if n.lower().endswith((".ps1", ".psm1")):
                        file.append(os.path.join(akar, n))
        else:
            hilang.append(p)
    return file, hilang


def main():
    ap = argparse.ArgumentParser(
        description="deteksi sintaks PS7 yang gagal di PowerShell 5.1")
    ap.add_argument("path", nargs="+", help="file .ps1/.psm1 atau folder")
    ap.add_argument("--json", action="store_true", help="output JSON")
    a = ap.parse_args()

    file, hilang = kumpul_file(a.path)
    hasil = []
    for f in file:
        try:
            teks = open(f, encoding="utf-8-sig").read()
        except OSError as ex:
            hilang.append(f)
            continue
        hasil.append({"file": f, "temuan": cari(teks)})

    total = sum(len(h["temuan"]) for h in hasil)
    if a.json:
        print(json.dumps({"file": hasil, "tidak_ditemukan": hilang,
                          "total": total}, indent=2, ensure_ascii=False))
    else:
        for h in hasil:
            for t in h["temuan"]:
                print(f"{h['file']}:{t['baris']}:{t['kolom']} "
                      f"[{t['aturan']}] {t['pesan']}")
        for p in hilang:
            print(f"[!] tidak ditemukan: {p}")
        print(f"[hasil] {total} temuan di {len(hasil)} file "
              f"({len(hilang)} path hilang)")
    if hilang:
        return 2
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
