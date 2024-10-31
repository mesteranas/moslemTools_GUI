from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
def playSoundEffect(path):
    sound=QSoundEffect()
    sound.setSource(QUrl(path))
    sound.play()