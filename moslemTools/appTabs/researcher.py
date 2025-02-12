import guiTools,pyperclip,winsound,json,functions,re,os,settings
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Albaheth(qt.QWidget):
    def __init__(self):
        super().__init__()                
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)        
        self.serch_laibol=qt.QLabel(_("ابحث في"))
        self.serch=qt.QComboBox()
        self.serch.addItem(_("القرآن الكريم"))
        self.serch.addItem(_("الأحاديث"))
        self.serch.setAccessibleName(_("ابحث في"))        
        self.ahadeeth_laibol=qt.QLabel(_("إختيار الكتاب"))
        self.ahadeeth=qt.QComboBox()
        self.ahadeeth.addItems(functions.ahadeeth.ahadeeths.keys())
        self.ahadeeth.setAccessibleName(_("إختيار الكتاب"))        
        self.serch.currentIndexChanged.connect(self.toggle_ahadeeth_visibility)
        self.serch_input=qt.QLineEdit()
        self.serch_input.setAccessibleName(_("أكتب محتوى البحث"))
        self.start=guiTools.QPushButton(_("البحث"))
        self.start.clicked.connect(self.onSearchClicked)
        self.results=guiTools.QReadOnlyTextEdit()                
        self.results.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.results.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=12
        font=self.font()
        font.setPointSize(self.font_size)
        self.results.setFont(font)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setText(str(self.font_size))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.serch_laibol)
        layout.addWidget(self.serch)
        layout.addWidget(self.ahadeeth_laibol)
        layout.addWidget(self.ahadeeth)
        layout.addWidget(qt.QLabel(_("أكتب محتوى البحث")))
        layout.addWidget(self.serch_input)
        layout.addWidget(self.start)
        layout.addWidget(self.results)        
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
        self.ahadeeth_laibol.hide()
        self.ahadeeth.hide()                    
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()        
        copy_all=menu.addAction(_("نسخ النص كاملا"))        
        copy_all.triggered.connect(self.copy_text)
        copy_selected_text=menu.addAction(_("نسخ النص المحدد"))
        copy_selected_text.triggered.connect(self.copy_line)
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)
        menu.addMenu(fontMenu)
        menu.exec(self.mapToGlobal(self.cursor().pos()))    
    def increase_font_size(self):
        self.font_size += 1
        guiTools.speak(str(self.font_size ))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        guiTools.speak(str(self.font_size ))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def update_font_size(self):
        cursor=self.results.textCursor()
        self.results.selectAll()
        font=self.results.font()
        font.setPointSize(self.font_size)
        self.results.setCurrentFont(font)        
        self.results.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.results.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.results.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def search(self,pattern,text_list):    
        tashkeel_pattern=re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670]')        
        normalized_pattern=tashkeel_pattern.sub('', pattern)        
        matches=[
            text for text in text_list
            if normalized_pattern in tashkeel_pattern.sub('', text)
        ]        
        return matches        
    def onSearchClicked(self):
        I=self.serch.currentIndex()
        if I==0:
            listOfWords=functions.quranJsonControl.getQuran()
        elif I==1:
            book_name=functions.ahadeeth.ahadeeths[self.ahadeeth.currentText()]
            with open(os.path.join(os.getenv('appdata'),settings.app.appName,"ahadeeth",book_name),"r",encoding="utf-8") as f:
                ahadeeth=json.load(f)
            listOfWords=[]
            for item in ahadeeth:
                listOfWords.append(str(ahadeeth.index(item)+1) + item)
        result=self.search(self.serch_input.text(),listOfWords)
        if result:
            self.results.setText("عدد نتائج البحث " + str(len(result)) + "\n" + "\n".join(result))
        else:
            self.results.setText(_("لم يتم العثور على نتائج"))
        self.results.setFocus()
    def toggle_ahadeeth_visibility(self):
        if self.serch.currentText() == _("الأحاديث"):
            self.ahadeeth_laibol.show()
            self.ahadeeth.show()
        else:
            self.ahadeeth_laibol.hide()
            self.ahadeeth.hide()