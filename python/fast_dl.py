# -*- coding: utf-8 -*-
"""Resumable multi-connection ranged downloader for EBI FTP (single stream too slow)."""
import os
import sys
import concurrent.futures as cf
import urllib.request

URL, OUT, NCHUNK = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 16

req = urllib.request.Request(URL, method="HEAD")
with urllib.request.urlopen(req, timeout=30) as r:
    size = int(r.headers["Content-Length"])
bounds = [(i * size // NCHUNK, (i + 1) * size // NCHUNK - 1 if i < NCHUNK - 1 else size - 1)
          for i in range(NCHUNK)]

def fetch(i):
    lo, hi = bounds[i]
    part = f"{OUT}.part{i:02d}"
    want = hi - lo + 1
    have = os.path.getsize(part) if os.path.exists(part) else 0
    if have == want:
        return i, want
    if have > want:
        os.remove(part); have = 0
    req = urllib.request.Request(URL, headers={"Range": f"bytes={lo + have}-{hi}"})
    with urllib.request.urlopen(req, timeout=60) as r, open(part, "ab") as f:
        while True:
            buf = r.read(1 << 20)
            if not buf:
                break
            f.write(buf)
    return i, os.path.getsize(part)

todo = [i for i in range(NCHUNK)
        if not os.path.exists(f"{OUT}.part{i:02d}")
        or os.path.getsize(f"{OUT}.part{i:02d}") != bounds[i][1] - bounds[i][0] + 1]
if todo:
    with cf.ThreadPoolExecutor(max_workers=NCHUNK) as ex:
        for i, got in ex.map(fetch, todo):
            pass
done = all(os.path.exists(f"{OUT}.part{i:02d}") and
           os.path.getsize(f"{OUT}.part{i:02d}") == bounds[i][1] - bounds[i][0] + 1
           for i in range(NCHUNK))
if done:
    with open(OUT, "wb") as out:
        for i in range(NCHUNK):
            with open(f"{OUT}.part{i:02d}", "rb") as p:
                while True:
                    b = p.read(1 << 22)
                    if not b:
                        break
                    out.write(b)
    for i in range(NCHUNK):
        os.remove(f"{OUT}.part{i:02d}")
    print("COMPLETE", OUT, size)
else:
    got = sum(os.path.getsize(f"{OUT}.part{i:02d}") for i in range(NCHUNK)
              if os.path.exists(f"{OUT}.part{i:02d}"))
    print(f"PARTIAL {got}/{size} ({100*got/size:.0f}%)")
