import os, stat, subprocess, shutil
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

debug = False
is_console = "console" if debug else "windowed"
build_cmd = f"""pyinstaller --noconfirm --onedir --{is_console} --icon "assets/app.ico" --name "ACGCAG" --clean --add-data ".venv/Lib/site-packages/customtkinter;customtkinter/" --add-data "assets;assets/" --add-data "LICENSE;."  "main.py" """

subprocess.run(build_cmd)

recommendation = """Thank you for using ACGCAG Launcher!

INSTALL RECOMMENDATIONS:
1. Head into the 'ACGCAG' folder and create a shortcut of the following:
    - file: ACGCAG.exe (you can rename this to whatever you want)

2. Move these to files to where you found this text file.
3. Enjoy not having to search endlessly through a lot of files to find the App!

NOTE:
You are free of using the app from within the folder without following the previous guide.
The previous guide is made to simplify locating and opening the app.
"""

disclaimer = """DISCLAIMER:
This software is just a file manager for GIMI skin mods. Neither ACGCAG or GIMI or 3DMigoto are held
responsible if you account gets banned.

Use at your own risk or use a private server.
"""

with open("dist/INSTALL_GUIDE.txt", "w") as f:
    f.write(recommendation)

with open("dist/DISCLAIMER-(READ-ME-FIRST).txt", "w") as f:
    f.write(disclaimer)


shutil.make_archive("ACGCAG-Launcher", "zip", "dist")
shutil.move("ACGCAG-Launcher.zip", "dist/ACGCAG-Launcher.zip")
