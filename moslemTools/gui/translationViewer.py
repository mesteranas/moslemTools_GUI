import functions,settings,guiTools,gettext,winsound,pyperclip
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
class translationViewer(qt.QDialog):
    def __init__(self,p,From,to):
        super().__init__(p)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                
        self.index=settings.settings_handler.get("translation","translation")
        self.From=From
        self.to=to        
        self.resize(1200,600)
        self.text=guiTools.QReadOnlyTextEdit()
        self.text.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.text.setFont(font)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setText(str(self.font_size))
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
        self.changetranslation=qt.QPushButton(_("تغيير الترجمة"))
        self.changetranslation.clicked.connect(self.on_change_translation)
        layout.addWidget(self.changetranslation)
        self.getResult()
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        save=menu.addAction(_("حفظ كملف نصي"))
        save.triggered.connect(self.save_text_as_txt)
        menu.setDefaultAction(save)
        print=menu.addAction(_("طباعة"))
        print.triggered.connect(self.print_text)
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
    def getResult(self):
        content=functions.translater.gettranslation(functions.translater.gettranslationByIndex(self.index),self.From,self.to)
        self.text.setText(content)
    def on_change_translation(self):
        menu=qt.QMenu(_("اختر #ترجمة"),self)
        translation=list(functions.translater.translations.keys())
        translation.remove(functions.translater.gettranslationByIndex(self.index))
        selectedtranslation=qt1.QAction(functions.translater.gettranslationByIndex(self.index),self)
        menu.addAction(selectedtranslation)
        menu.setDefaultAction(selectedtranslation)
        selectedtranslation.setCheckable(True)
        selectedtranslation.setChecked(True)
        selectedtranslation.triggered.connect(lambda:self.ontranslationChanged(functions.translater.gettranslationByIndex(self.index)))
        for t in translation:
            tAction=qt1.QAction(t,self)
            tAction.triggered.connect(lambda:self.ontranslationChanged(t))
            menu.addAction(tAction)
        menu.setAccessibleName(_("اختر ترجمة"))
        menu.setFocus()
        menu.exec()
    def ontranslationChanged(self,name:str):
        self.index=functions.translater.translations[self.sender().text()]
        self.getResult()
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
        guiTools.speak(str(self.font_size ))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        guiTools.speak(str(self.font_size ))
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