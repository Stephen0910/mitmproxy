#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path

here = Path(__file__).parent

for script in sorted((here / "scripts").glob("*.py")):
    print(f"Generating output for {script.name}...")
    out = subprocess.check_output(["python", script.absolute()], cwd=here, text=True)
    if out:
        (here / "src" / "generated" / f"{script.stem}.html").write_text(
            out, encoding="utf8"
        )

if (here / "public").exists():
    shutil.rmtree(here / "public")
subprocess.run([r"E:\Program\hugo_extended\hugo.exe"], cwd=here / "src", check=True)
