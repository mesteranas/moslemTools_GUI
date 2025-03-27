import shutil
import os
import subprocess
if os.path.exists("moslemTools_build"):
    print("removing moslemTools_build")
    shutil.rmtree("moslemTools_build")
# Create a version resource file for Windows executables.
version_info = r'''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# https://docs.microsoft.com/en-us/windows/win32/menurc/vs-versioninfo
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(7, 0, 0, 0),
    prodvers=(7, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',
          [
            StringStruct('CompanyName', 'mister anas , abd el-rahman mohammed alcoder'),
            StringStruct('FileDescription', 'moslem tools , the best program for moslems'),
            StringStruct('FileVersion', '7.0.0.0'),
            StringStruct('InternalName', 'moslem tools'),
            StringStruct('OriginalFilename', 'moslem_tools.exe'),
            StringStruct('ProductName', 'moslem tools'),
            StringStruct('ProductVersion', '7.0.0.0'),
            StringStruct('LegalCopyright', '© 2025 ; moslem tools developers')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
'''

# Write version info to a file.
version_file_path = "version_file.txt"
with open(version_file_path, "w", encoding="utf-8") as vf:
    vf.write(version_info.strip())

include_files = [
    ("data/dlls", "data/dlls"),
    ("data/icons", "data/icons"),
    ("data/sounds/adaan", "data/sounds/adaan"),
    ("data/sounds/athkar", "data/sounds/athkar"),
    ("data/sounds/001001.mp3", "data/sounds/001001.mp3"),
    ("data/sounds/next_page.wav", "data/sounds/next_page.wav"),
    ("data/sounds/prayAfterAdaan.m4a", "data/sounds/prayAfterAdaan.m4a"),
    ("data/sounds/previous_page.wav", "data/sounds/previous_page.wav"),
    ("data/json/files", "data/json/files"),
    ("data/json/quranRecitations", "data/json/quranRecitations"),
    ("data/json/ahadeeth/nawawi40.json", "data/json/ahadeeth/nawawi40.json"),
    ("data/json/ahadeeth/qudsi40.json", "data/json/ahadeeth/qudsi40.json"),
    ("data/json/islamicBooks/elShabahLibe.json", "data/json/islamicBooks/elShabahLibe.json"),
    ("data/json/Quran Translations/en.itani.json", "data/json/Quran Translations/en.itani.json"),
    ("data/json/tafaseer/muyassar.json", "data/json/tafaseer/muyassar.json"),
    ("data/json/athkar.json", "data/json/athkar.json"),
    ("data/json/i raab.json", "data/json/i raab.json"),
    ("data/json/namesOfAllah.json", "data/json/namesOfAllah.json"),
    ("data/json/prophetStories.json", "data/json/prophetStories.json"),
    ("data/json/quran.json", "data/json/quran.json"),
    ("data/json/quranStories.json", "data/json/quranStories.json"),
    ("data/json/reciters.json", "data/json/reciters.json"),
    ("data/json/tanzil.json", "data/json/tanzil.json"),
    ("data/json/text_athkar.json", "data/json/text_athkar.json")
]

# Dynamically add language resource files from the "data/languages" folder.
for languageFolder in os.listdir("data/languages"):
    languagesFolder = os.path.join("data", "languages", languageFolder)
    if os.path.isdir(languagesFolder):
        langNameFile = os.path.join(languagesFolder, "langName.translation")
        langContent = os.path.join(languagesFolder, "LC_MESSAGES", "moslemTools_GUI.mo")
        include_files.append((langNameFile, langNameFile))
        include_files.append((langContent, langContent))

print("Converting to exe, please wait...")

# Run PyInstaller with windowed mode, icon, and version file options.
command = [
    "pyinstaller",
    "-w",
    "--icon=data/icons/app_icon.ico",
    f"--version-file={version_file_path}",
    "moslem_tools.py"
]

run = subprocess.run(command)

if run.returncode == 0:
    print("PyInstaller build successful.")
    # Assuming that the built executable is in the folder "dist/moslem_tools"
    target_dir = os.path.join("dist", "moslem_tools")
    for src, dest in include_files:
        dest_path = os.path.join(target_dir, dest)
        dest_folder = os.path.dirname(dest_path)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        try:
            if os.path.isdir(src):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src, dest_path)
            else:
                shutil.copy2(src, dest_path)
            print(f"Copied {src} to {dest_path}")
        except Exception as e:
            print(f"Error copying {src} to {dest_path}: {e}")
    print("All include files have been copied.")
else:
    print("PyInstaller build failed.")
print("removing version file")
try:
    os.remove(version_file_path )
    print
    ("removed")
except:
    print("error while removing")
print("removing build folder")
try:
    shutil.rmtree("build")
    print("done")
except:
    print("error")
print("removing moslem_tools.spec")
try:
    os.remove("moslem_tools.spec")
    print("done")
except:
    print("error")
print("editing some files")
try:
    shutil.copytree("dist/moslem_tools","moslemTools_build")
    print("done")
    shutil.rmtree("dist")
    print("done")
except:
    print("error")