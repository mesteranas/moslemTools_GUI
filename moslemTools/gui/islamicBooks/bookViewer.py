import guiTools,pyperclip,winsound,gettext,json,functions,settings,os
import PyQt6.QtWidgets as qt
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
class book_viewer(qt.QDialog):
    def __init__(self,p,book_name,partName:str,content:list,index:int=0):
        super().__init__(p)
        self.setWindowState(qt2.Qt.WindowState.WindowMaximized)
        self.data=content
        self.index=index
        self.bookName=book_name
        self.part=partName
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                        
        qt1.QShortcut("alt+right",self).activated.connect(self.next_book)
        qt1.QShortcut("alt+left",self).activated.connect(self.previous_book)
        qt1.QShortcut("ctrl+g",self).activated.connect(self.go_to_book)
        qt1.QShortcut("ctrl+b",self).activated.connect(self.onAddOrRemoveBookmark)
        self.resize(1200,600)
        self.text=guiTools.QReadOnlyTextEdit()        
        self.text.setText(self.data[self.index])
        self.text.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=12
        font=self.font()
        font.setPointSize(self.font_size)
        self.text.setFont(font)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.font_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.show_font.setText(str(self.font_size))
        self.N_book=qt.QPushButton(_("الصفحة التالية"))
        self.N_book.setAccessibleDescription(_("alt زائد السهم الأيمن"))
        self.N_book.clicked.connect(self.next_book)        
        self.P_book=qt.QPushButton(_("الصفحة السابقة"))
        self.P_book.setAccessibleDescription(_("alt زائد السهم الأيسر"))
        self.P_book.clicked.connect(self.previous_book)
        self.P_book.setStyleSheet("background-color: #0000AA; color: white;")
        self.N_book.setStyleSheet("background-color: #0000AA; color: white;")
        self.book_number_laybol=qt.QLabel(_("رقم الصفحة"))
        self.book_number_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.show_book_number=qt.QLineEdit()
        self.show_book_number.setReadOnly(True)
        self.show_book_number.setAccessibleName(_("رقم الصفحة"))
        self.show_book_number.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.show_book_number.setText(str(self.index+1))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)        
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
        layout.addWidget(self.book_number_laybol)
        layout.addWidget(self.show_book_number)
        layout1=qt.QHBoxLayout()
        layout1.addWidget(self.P_book)
        layout1.addWidget(self.N_book)
        layout.addLayout(layout1)
    def next_book(self):
        if self.index == len(self.data)-1:
            self.index=0
        else:
            self.index+=1
        self.text.setText(self.data[self.index])
        guiTools.speak(str(self.index+1))
        self.show_book_number.setText(str(self.index+1))
        winsound.PlaySound("data/sounds/next_page.wav",1)
    def previous_book(self):
        if self.index == 0:
            self.index=len(self.data)-1
        else:
            self.index-=1
        self.text.setText(self.data[self.index])
        guiTools.speak(str(self.index+1))
        self.show_book_number.setText(str(self.index+1))
        winsound.PlaySound("data/sounds/previous_page.wav",1)
    def go_to_book(self):        
        book,OK=qt.QInputDialog.getInt(self,_("الذهاب إلى صفحة"),_("أكتب رقم الصفحة"),self.index+1,1,len(self.data))
        if OK:                                    
            self.index=book-1
            self.text.setText(self.data[self.index])
            self.show_book_number.setText(str(self.index+1))
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"), self)
        boldFont=menu.font()
        boldFont.setBold(True)
        menu.setFont(boldFont)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        book_menu=qt.QMenu(_("خيارات الصفحة"), self)
        next_action=book_menu.addAction(_("الصفحة التالية"))
        next_action.triggered.connect(self.next_book)
        previous_action=book_menu.addAction(_("الصفحة السابقة"))
        previous_action.triggered.connect(self.previous_book)
        go_action=book_menu.addAction(_("الذهاب إلى صفحة"))
        go_action.triggered.connect(self.go_to_book)
        state,self.nameOfBookmark=functions.bookMarksManager.getIslamicBookBookmarkName(self.bookName,self.index)
        if state:
            removeBookmarkAction=qt1.QAction(_("حذف العلامة المرجعية"),self)
            book_menu.addAction(removeBookmarkAction)
            removeBookmarkAction.triggered.connect(self.onRemoveBookmark)
        else:
            addBookMarkAction=qt1.QAction(_("إضافة علامة مرجعية"),self)
            book_menu.addAction(addBookMarkAction)
            addBookMarkAction.triggered.connect(self.onAddBookMark)
        menu.addMenu(book_menu)
        text_options_menu=qt.QMenu(_("خيارات النص"), self)
        save_action=text_options_menu.addAction(_("حفظ كملف نصي"))
        save_action.triggered.connect(self.save_text_as_txt)
        text_options_menu.setDefaultAction(save_action)
        print_action=text_options_menu.addAction(_("طباعة"))
        print_action.triggered.connect(self.print_text)
        copy_all_action=text_options_menu.addAction(_("نسخ النص كاملاً"))
        copy_all_action.triggered.connect(self.copy_text)
        copy_selected_action=text_options_menu.addAction(_("نسخ النص المحدد"))
        copy_selected_action.triggered.connect(self.copy_line)    
        font_menu=qt.QMenu(_("حجم الخط"), self)
        increase_font_action=qt1.QAction(_("تكبير الخط"), self)
        font_menu.addAction(increase_font_action)
        increase_font_action.triggered.connect(self.increase_font_size)
        decrease_font_action=qt1.QAction(_("تصغير الخط"), self)
        font_menu.addAction(decrease_font_action)
        decrease_font_action.triggered.connect(self.decrease_font_size)            
        menu.addMenu(text_options_menu)
        menu.addMenu(font_menu)
        text_options_menu.setFont(boldFont)
        font_menu.setFont(boldFont)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def print_text(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.text.print(printer)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def save_text_as_txt(self):
        try:
            file_dialog=qt.QFileDialog()
            file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
            file_dialog.setDefaultSuffix("txt")
            if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
                file_name=file_dialog.selectedFiles()[0]
                with open(file_name, 'w', encoding='utf-8') as file:
                    text = self.text.toPlainText()
                    file.write(text)                
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def increase_font_size(self):
        if self.font_size < 50:
            self.font_size += 1
            guiTools.speak(str(self.font_size))
            self.show_font.setText(str(self.font_size))
            self.update_font_size()
    def decrease_font_size(self):
        if self.font_size > 1:
            self.font_size -= 1
            guiTools.speak(str(self.font_size))
            self.show_font.setText(str(self.font_size))
            self.update_font_size()
    def update_font_size(self):
        cursor=self.text.textCursor()
        self.text.selectAll()
        font=self.text.font()
        font.setPointSize(self.font_size)
        self.text.setCurrentFont(font)        
        self.text.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.text.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.text.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def onAddBookMark(self):
        name,OK=guiTools.QInputDialog.getText(self,_("إضافة علامة مرجعية"),_("أكتب أسم للعلامة المرجعية"))
        if OK:
            functions.bookMarksManager.addNewislamicBookBookMark(self.bookName,self.part,self.index,name)
    def onRemoveBookmark(self):
        try:
            functions.bookMarksManager.removeislamicBookBookMark(self.nameOfBookmark)
            winsound.Beep(1000,100)
        except:
            qt.QMessageBox.critical(self,_("خطأ"),_("تعذر حذف العلامة المرجعية"))
    def onAddOrRemoveBookmark(self):
        state,self.nameOfBookmark=functions.bookMarksManager.getIslamicBookBookmarkName(self.bookName,self.index)
        if state:
            self.onRemoveBookmark()
        else:
            self.onAddBookMark()