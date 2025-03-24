import shutil
import sys
import os
import PyQt6.QtPrintSupport
from cx_Freeze import setup, Executable
import PyQt6
pyqt_path = os.path.dirname(PyQt6.__file__)
include_files = [
    ("data/dlls", "data/dlls"),
    ("data/icons","data/icons"),
    ("data/sounds/adaan","data/sounds/adaan"),
    ("data/sounds/athkar","data/sounds/athkar"),
    ("data/sounds/001001.mp3","data/sounds/001001.mp3"),
    ("data/sounds/next_page.wav","data/sounds/next_page.wav"),
    ("data/sounds/prayAfterAdaan.m4a","data/sounds/prayAfterAdaan.m4a"),
    ("data/sounds/previous_page.wav","data/sounds/previous_page.wav"),
    ("data/json/files","data/json/files"),
    ("data/json/quranRecitations","data/json/quranRecitations"),
    ("data/json/ahadeeth/nawawi40.json","data/json/ahadeeth/nawawi40.json"),
    ("data/json/ahadeeth/qudsi40.json","data/json/ahadeeth/qudsi40.json"),
    ("data/json/islamicBooks/elShabahLibe.json","data/json/islamicBooks/elShabahLibe.json"),
    ("data/json/Quran Translations/en.itani.json","data/json/Quran Translations/en.itani.json"),
    ("data/json/tafaseer/muyassar.json","data/json/tafaseer/muyassar.json"),
    ("data/json/athkar.json","data/json/athkar.json"),
    ("data/json/i raab.json","data/json/i raab.json"),
    ("data/json/namesOfAllah.json","data/json/namesOfAllah.json"),
    ("data/json/prophetStories.json","data/json/prophetStories.json"),
    ("data/json/quran.json","data/json/quran.json"),
    ("data/json/quranStories.json","data/json/quranStories.json"),
    ("data/json/reciters.json","data/json/reciters.json"),
    ("data/json/tanzil.json","data/json/tanzil.json"),
    ("data/json/text_athkar.json","data/json/text_athkar.json")
]
for languageFolder in os.listdir("data/languages"):
    languagesFolder="data/languages/" + languageFolder
    if os.path.isdir(languagesFolder):
        langNameFile=languagesFolder + "/langName.translation"
        langcontent=languagesFolder + "/LC_MESSAGES/moslemTools_GUI.mo"
        include_files.append((langNameFile,langNameFile))
        include_files.append((langcontent,langcontent))
dll_files = ["Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll", "Qt6Network.dll","","Qt6Multimedia.dll","Qt6MultimediaQuick.dll","Qt6PrintSupport.dll"]
for file in dll_files:
    include_files.append((os.path.join(pyqt_path, "Qt6", "bin", file), os.path.join("lib", file)))


build_exe_options = {
    "build_exe": "moslemTools_build",
    "optimize": 1,
    "include_files": include_files,
    "packages": ["appTabs", "functions", "gui","settings","update","guiTools"],
    "includes": ["PyQt6.QtCore", "PyQt6.QtWidgets", "PyQt6.QtGui", "PyQt6.QtMultimedia", "PyQt6.QtPrintSupport","packaging", "requests","hijri_converter","notifypy","geocoder","pyperclip","win32com.client"],
    "excludes": ["tkinter", "test", "setuptools", "pip", "numpy", "unittest"],
    "include_msvcr": True
}

setup(
    name="moslemTools",
    version="7.0.0",
    description="moslem tools",
    long_description="moslem tools , all islamic tools in one place",
    author="mister anas , abd el-rahman mohamed alcoder",
    url="https://github.com/mesteranas/moslemTools_GUI/",
    download_url="https://github.com/mesteranas/moslemTools_GUI/",
    keywords=["islamic", "islam", "quran", "desktop", "alquran", "hadeeth", "القرآن", "إسلام","حديث"],
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "moslem_tools.py",
            base="Win32GUI" if sys.platform == "win32" else None,
            target_name="moslemTools.exe",
            icon="data/icons/app_icon.ico",
            copyright="2025 moslem tooles developers"
        )
    ]
)

folder_paths = ["moslemTools_build/lib/PyQt6/Qt6/bin", "moslemTools_build/lib/PyQt6/Qt6/translations"]
for folder in folder_paths:
    try:
        shutil.rmtree(os.path.abspath(folder))
    except Exception as e:
        print(f"Error removing {folder}: {e}")

