import gettext
from collections import OrderedDict
from .settings_handler import get,appName

def init_translation():
	try:
		translation=gettext.translation(appName, localedir='data/languages', languages=[get("g","lang")])
	except:
		translation=gettext.translation(appName, fallback=True)
	translation.install()
def lang():
	supported_languages = OrderedDict({
		"العربية": "ar",
	})
	import os
	l=os.listdir("data/languages")
	for i in l:
		try:
			with open(f"data/languages/{i}/langName.translation","r",encoding="utf-8") as f:
				a=f.read()
			supported_languages[a]=i
		except:
			pass
	return supported_languages
