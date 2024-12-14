import guiTools,webbrowser
from settings import *
import PyQt6.QtWidgets as qt
language.init_translation()
class About_developers(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.info=guiTools.QListWidget()
        self.info.itemClicked.connect(self.open_link)        
        self.info.addItem(_("عبد الرحمن محمد alcoder"))
        self.info.addItem(_("قناة عبد الرحمن على YouTube"))
        self.info.addItem(_("حساب عبد الرحمن على telegram"))
        self.info.addItem(_("حساب عبد الرحمن على GitHub"))
        self.info.addItem(_("أنس محمد"))
        self.info.addItem(_("قناة أنس على telegram"))
        self.info.addItem(_("حساب أنس على telegram"))
        self.info.addItem(_("حساب أنس على GitHub"))
        self.info.addItem(_("التواصل مع أنس عبر البريد الإكتروني"))        
        self.info.addItem(_("فيديو شرح البرنامج على YouTube"))
        self.info_text=qt.QLineEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setText(_("اللهم اجعل عملنا هذا في ميزان حسناتنا وصدقة جارية لنا"))
        layout=qt.QVBoxLayout()
        layout.addWidget(self.info)
        layout.addWidget(self.info_text)
        self.setLayout(layout)                
    def open_link(self):    
        current_item=self.info.currentItem()
        if current_item:
            text=current_item.text()
            if text == _("قناة عبد الرحمن على YouTube"):
                webbrowser.open("https://youtube.com/@alcoder01?feature=shared")
            elif text == _("حساب عبد الرحمن على telegram"):
                webbrowser.open("https://t.me/P1_1_1")
            elif text == _("حساب عبد الرحمن على GitHub"):
                webbrowser.open("https://github.com/MesterAbdAlrhmanMohmed")
            elif text == _("قناة أنس على telegram"):
                webbrowser.open("https://t.me/tprogrammers")
            elif text == _("حساب أنس على telegram"):
                webbrowser.open("https://t.me/mesteranasm")
            elif text == _("حساب أنس على GitHub"):
                webbrowser.open("https://github.com/mesteranas/")
            elif text == _("التواصل مع أنس عبر البريد الإكتروني"):
                webbrowser.open("mailto:anasformohammed@gmail.com")
            elif text == _("فيديو شرح البرنامج على YouTube"):
                webbrowser.open("https://www.youtube.com/watch?v=NUe8ftmg4Cw")