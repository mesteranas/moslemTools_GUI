from settings import settings_handler
import guiTools,gui,gettext
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Download(qt.QDialog):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.types=guiTools.QListWidget()
        self.types.addItems([_("كتاب تفسير"),_("ترجمة قرآن"),_("كتاب حديث"),_("قارئ للقرآن المكتوب"),_("أذكار وأدعية"),_("الكتب الإسلامية")])
        self.types.clicked.connect(self.onItemClicked)
        self.adminstration=qt.QLineEdit()
        self.adminstration.setReadOnly(True)
        self.adminstration.setText(_("تنبيه هام , لتثبيت موارد خارجية, يجب أولا منح صلاحيات المشرف للبرنامج"))
        self.adminstration.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.types)
        layout.addWidget(self.adminstration)
    def onItemClicked(self):
        index=self.types.currentRow()
        if index==0:
            gui.download.SelectItem(self,"all_tafaseers.json","tafaseer").exec()
        elif index==1:    
            gui.download.SelectItem(self,"all_translater.json","Quran Translations").exec()
        elif index==2:    
            gui.download.SelectItem(self,"all_ahadeeth.json","ahadeeth").exec()        
        elif index==3:
            gui.download.SelectReciter(self).exec()
        elif index==4:
            gui.download.SelectAthkar(self).exec()
        elif index==5:
            gui.download.SelectItem(self,"all_islamic_books.json","islamicBooks").exec()