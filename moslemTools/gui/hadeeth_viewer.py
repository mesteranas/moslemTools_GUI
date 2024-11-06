import guiTools,pyperclip,winsound,gettext,json
import PyQt6.QtWidgets as qt
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
_=gettext.gettext
class hadeeth_viewer(qt.QDialog):
    def __init__(self,p,book_name):
        super().__init__(p)
        with open("data/json/ahadeeth/"+book_name,"r",encoding="utf-8") as f:
            self.data=json.load(f)    
        self.index=0        
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                        
        qt1.QShortcut("alt+right",self).activated.connect(self.next_hadeeth)
        qt1.QShortcut("alt+left",self).activated.connect(self.previous_hadeeth)
        qt1.QShortcut("ctrl+g",self).activated.connect(self.go_to_hadeeth)
        self.font_size=20
        self.showFullScreen()
        self.text=guiTools.QReadOnlyTextEdit()        
        self.text.setText(self.data[self.index])
        self.text.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.OnContextMenu)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)        
    def next_hadeeth(self):
        if self.index == len(self.data)-1:
            self.index=0
        else:
            self.index+=1
        self.text.setText(self.data[self.index])
        guiTools.speak(str(self.index+1))
        winsound.PlaySound("data/sounds/next_page.wav",1)
    def previous_hadeeth(self):
        if self.index == 0:
            self.index=len(self.data)-1
        else:
            self.index-=1
        self.text.setText(self.data[self.index])
        guiTools.speak(str(self.index+1))
        winsound.PlaySound("data/sounds/previous_page.wav",1)
    def go_to_hadeeth(self):        
        hadeeth,OK=qt.QInputDialog.getInt(self,_("الذهاب إلى حديث"),_("أكتب رقم الحديث"),self.index+1,1,len(self.data))
        if OK:                                    
            self.index=hadeeth-1
            self.text.setText(self.data[self.index])
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"), self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        hadeeth_menu=qt.QMenu(_("خيارات الحديث"), self)
        next_action=hadeeth_menu.addAction(_("الحديث التالي"))
        next_action.triggered.connect(self.next_hadeeth)
        previous_action=hadeeth_menu.addAction(_("الحديث السابق"))
        previous_action.triggered.connect(self.previous_hadeeth)
        go_action=hadeeth_menu.addAction(_("الذهاب إلى حديث"))
        go_action.triggered.connect(self.go_to_hadeeth)
        menu.addMenu(hadeeth_menu)
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
        self.font_size += 1
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
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