#!/usr/bin/env python3
"""Export translations for native-speaker review, and import corrections back.
  python3 review_kit.py export <out_dir>     -> review-<lang>.csv (UTF-8 with BOM, opens in Excel/Sheets)
  python3 review_kit.py import <csv> <lang>  -> writes the 'Corrected' column into build/i18n/<lang>.py
Reviewers only fill the 'Corrected' column (leave it empty when the current text is fine)."""
import csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from i18n import en, hi, te, kn, ta, ml
MODS = {"hi": hi, "te": te, "kn": kn, "ta": ta, "ml": ml}
NAMES = {"hi": "Hindi", "te": "Telugu", "kn": "Kannada", "ta": "Tamil", "ml": "Malayalam"}
HERE = pathlib.Path(__file__).parent / "i18n"
NOTE = {
 "brand.lab": "Native-script word for 'Prayogashala' (laboratory). Brand word shown in the hero and footer.",
 "brand.marga": "Native-script word for MARGA ('path'), shown beside the name MARGA.",
 "d.marga": "Contains the word for 'path'; keep consistent with brand.marga.",
 "tools.sub": "{n} is replaced by a number. Keep {n}.",
 "stops.n": "{n} is replaced by a number. Keep {n}.",
 "dr.tag": "{n} is replaced by a number like 01. Keep {n}.",
 "hero.h1a": "First half of the headline (keep trailing space). Reads together with hero.h1b: 'Technology, open to everyone.'",
 "hero.h1b": "Second half of the headline, shown in gold.",
 "theme.new": "Name of the third colour theme (a new teal look). Short word.",
 "w.docker.t": "Product names (Docker, Kubernetes ...) stay in English; translate only the word 'Lab'.",
}
def export(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    for code, m in MODS.items():
        with open(out / f"review-{code}.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Key", "English", f"Current {NAMES[code]}", f"Corrected {NAMES[code]} (leave empty if fine)", "Note"])
            for k, v in en.T.items():
                if k == "brand.marga": v = "(empty in English)"
                w.writerow([k, v, m.T[k], "", NOTE.get(k, "")])
    print("wrote", len(MODS), "files to", out)
def imp(csv_path, code):
    m = MODS[code]; T = dict(m.T); n = 0
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row[0] in T and len(row) > 3 and row[3].strip():
                T[row[0]] = row[3].strip(); n += 1
    body = "T = {\n" + "".join(f" {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in T.items()) + "}\n"
    (HERE / f"{code}.py").write_text(body, encoding="utf-8")
    print(f"{code}: applied {n} corrections. Now run build.py and verify.py.")
if __name__ == "__main__":
    if sys.argv[1] == "export": export(sys.argv[2])
    elif sys.argv[1] == "import": imp(sys.argv[2], sys.argv[3])
