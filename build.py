import os, stat, subprocess
from pathlib import Path


def super_rmtree(path: Path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)


dist = Path("dist")

if not dist.exists():
    dist.mkdir()
else:
    super_rmtree(dist)

use_console = False
is_console = "console" if use_console else "windowed"
build_cmd = f"""pyinstaller --noconfirm --onedir --{is_console} --icon "assets/app.ico" --name "ACGCAG" --clean --add-data ".venv/Lib/site-packages/customtkinter;customtkinter/" --add-data "assets;assets/" --add-data "LICENSE;."  "main.py" """

subprocess.run(build_cmd)
os.symlink(Path("ACGCAG/ACGCAG.exe"), Path("dist/Launcher.exe"))
os.symlink(Path("ACGCAG/assets"), Path("dist/assets"), True)
