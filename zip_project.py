import zipfile
from pathlib import Path

def zip_project():
    BASE = Path(".")
    zip_path = BASE.with_suffix(".zip")
    print(f"\n[OK] Zipping project to: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in BASE.rglob("*"):
            if file.is_file():
                zipf.write(file, arcname=file.relative_to(BASE))
    print("[OK] ZIP complete.")

if __name__ == "__main__":
    zip_project()
