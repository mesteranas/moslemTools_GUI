import gui,guiTools,functions,os,json,re
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class IslamicBooks(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        qt1.QShortcut("f5",self).activated.connect(self.refresh)
        serch=qt.QLabel(_("بحث"))
        serch.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(serch)
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        self.search_bar.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.search_bar)
        self.list_of_abook=guiTools.QListWidget()
        self.list_of_abook.addItems(functions.islamicBooks.books.keys())
        self.list_of_abook.itemClicked.connect(self.open)
        layout.addWidget(self.list_of_abook)
        self.info=qt.QLineEdit()
        self.info.setReadOnly(True)
        self.info.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.info.setText(_("في حالة تحميل كتاب جديد, يرجى إعادة تحميل قائمة الكتب بالضغت على زر F5"))
        layout.addWidget(self.info)
        self.info1=qt.QLineEdit()
        self.info1.setReadOnly(True)
        self.info1.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.info1.setText(_("تنبيه هام , مطوري البرنامج غير مسؤولين عن محتوى هذه الكتب"))
        layout.addWidget(self.info1)
        self.info2=qt.QLineEdit()
        self.info2.setReadOnly(True)
        self.info2.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.info2.setText(_("لحذف أي كتاب تم تحميله, نستخدم زر الحذف أو زر التطبيقات"))
        layout.addWidget(self.info2)
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
    def refresh(self):
        functions.islamicBooks.setbook()
        self.list_of_abook.clear()
        self.list_of_abook.addItems(functions.islamicBooks.books.keys())
    def search(self,pattern,text_list):    
        tashkeel_pattern=re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670]')        
        normalized_pattern=tashkeel_pattern.sub('', pattern)        
        matches=[
            text for text in text_list
            if normalized_pattern in tashkeel_pattern.sub('', text)
        ]        
        return matches        
    def onsearch(self):
        search_text=self.search_bar.text().lower()
        self.list_of_abook.clear()
        result=self.search(search_text,list(functions.islamicBooks.books.keys()))
        self.list_of_abook.addItems(result)
