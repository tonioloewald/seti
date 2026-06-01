#!/usr/bin/env python3
"""Step 3 input: fetch the Bergeron/Montreal white-dwarf synthetic-photometry
grids (Bedard et al. 2020) — the §5.3 H0 atmosphere model.

These tabulate absolute magnitudes vs (Teff, log g) in many bands, including the
Gaia EDR3 (G3, G3_BP, G3_RP) and WISE (W1-W4) bands we use to predict the
photospheric IR flux. They are small (~100 KB each) static reference grids, so —
unlike survey data — they ARE committed (data/models/bergeron/), pinning the exact
photosphere model used.
"""
import hashlib, os, urllib.request

BASE = "http://www.astro.umontreal.ca/~bergeron/CoolingModels/Tables"
FILES = ["Table_DA", "Table_DB"]  # pure-H (DA) and pure-He (DB) grids
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(ROOT, "data", "models", "bergeron")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    os.makedirs(DEST, exist_ok=True)
    sums = {}
    for name in FILES:
        dest = os.path.join(DEST, name)
        if not os.path.exists(dest):
            url = f"{BASE}/{name}"
            print(f"  downloading {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "seti-wd-search/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as out:
                out.write(r.read())
        sums[name] = sha256(dest)
        print(f"  {sums[name]}  {name} ({os.path.getsize(dest)//1024} KB)")
    with open(os.path.join(DEST, "SHA256SUMS"), "w") as f:
        for name in FILES:
            f.write(f"{sums[name]}  {name}\n")
    print(f"  -> {DEST} (committed)")


if __name__ == "__main__":
    main()
