import gui,guiTools,functions,os,json
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class IslamicBooks(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_abook=guiTools.QListWidget()
        self.list_of_abook.addItems(functions.islamicBooks.books.keys())
        self.list_of_abook.itemClicked.connect(self.open)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_abook)
        self.list_of_abook.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_of_abook.customContextMenuRequested.connect(self.onDelete)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
    def onDelete(self):
        selectedItem=self.list_of_abook.currentItem()
        if selectedItem:
            itemText=selectedItem.text()
            if itemText=="حياة الصحابة":
                qt.QMessageBox.critical(self,_("تنبيه"),_("لا يمكنك حذف هذا الكتاب "))
            else:
                question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف هذا الكتاب"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
                if question==qt.QMessageBox.StandardButton.Yes:
                    name=functions.islamicBooks.books[itemText]
                    os.remove(os.path.join(os.getenv('appdata'),app.appName,"islamicBooks",name))
                    functions.islamicBooks.setbook()
                    self.list_of_abook.clear()
                    self.list_of_abook.addItems(functions.islamicBooks.books.keys())
                    guiTools.speak(_("تم الحذف"))
    def open(self):
        try:
            with open(os.path.join(os.getenv('appdata'),app.appName,"islamicBooks",functions.islamicBooks.books[self.list_of_abook.currentItem().text()]),"r",encoding="utf-8") as f:
                data=json.load(f)    
                bookName=functions.islamicBooks.books[self.list_of_abook.currentItem().text()]
                if len(list(data.keys()))==1:
                    partName=list(data.keys())[0]
                    gui.islamicBooks.book_viewer(self,bookName,partName,data[partName]).exec()
                else:
                    gui.islamicBooks.PartSelection(self,bookName,data).exec()
        except Exception as error:
            print(error)
            qt.QMessageBox.critical(self,_("خطأ"),_("تعذر فتح الملف "))
