import os
os.add_dll_directory(os.path.join(os.getcwd(),"data","dlls"))
import ctypes
nvda = ctypes.windll.LoadLibrary(os.path.join(os.getcwd(),"data","dlls","nvda_speak.dll"))
def speak(msg):
	running = nvda.nvdaController_testIfRunning()
	if running != 1:
		nvda.nvdaController_speakText(msg)
	print(msg)