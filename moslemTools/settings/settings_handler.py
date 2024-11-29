from configparser import ConfigParser
import os,shutil
from . import app
appName=app.appName
if not os.path.exists(os.path.join(os.getenv('appdata'),appName,"quran surah reciters")):
	os.mkdir(os.path.join(os.getenv('appdata'),appName,"quran surah reciters"))
if not os.path.exists(os.path.join(os.getenv('appdata'),appName,"athkar")):
	os.mkdir(os.path.join(os.getenv('appdata'),appName,"athkar"))
if not os.path.exists(os.path.join(os.getenv('appdata'),appName,"Quran Translations")):
	os.mkdir(os.path.join(os.getenv('appdata'),appName,"Quran Translations"))
if not os.path.exists(os.path.join(os.getenv('appdata'),appName,"reciters")):
	os.mkdir(os.path.join(os.getenv('appdata'),appName,"reciters"))
if not os.path.exists(os.path.join(os.getenv('appdata'),appName,"tafaseer")):
	os.mkdir(os.path.join(os.getenv('appdata'),appName,"tafaseer"))
if not os.path.exists(os.path.join(os.getenv('appdata'),appName,"ahadeeth")):
	os.mkdir(os.path.join(os.getenv('appdata'),appName,"ahadeeth"))
cpath=os.path.join(os.getenv('appdata'),appName,"settings.ini")
if not os.path.exists(os.path.join(os.getenv('appdata'),appName)):
	os.mkdir(os.path.join(os.getenv('appdata'),appName))
if not os.path.exists(cpath):
	config = ConfigParser() 
	config.add_section("g")
	config["g"]["lang"] = "ar"
	config["g"]["exitDialog"] = "True"
	config["g"]["reciter"]="0"
	config.add_section("tafaseer")
	config["tafaseer"]["tafaseer"]="jalalayn.json"
	config.add_section("translation")
	config["translation"]["translation"]="en.ahmedali.json"
	config.add_section("athkar")
	config["athkar"]["voice"]="0"
	config["athkar"]["text"]="0"
	config.add_section("update")
	config["update"]["autoCheck"]="True"
	config["update"]["beta"]="False"
	with open(cpath, "w",encoding="utf-8") as file:
		config.write(file)

def get(section,key):
	try:
		config = ConfigParser()
		config.read(cpath)
		value = config[section][key]
		return value
	except:
		return ""

def set(section,key, value):
		config = ConfigParser()
		config.read(cpath)
		config[section][key] = value
		with open(cpath, "w",encoding="utf-8") as file:
			config.write(file)

