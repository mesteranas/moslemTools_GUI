import guiTools,pyperclip,winsound
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
class UserGuide(qt.QWidget):
    def __init__(self):
        super().__init__()                
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                
        self.guide=guiTools.QReadOnlyTextEdit()        
        self.guide.setText(_("دليل المستخدم لبرنامج Moslem Tools\n\nمقدمة\nبرنامج Moslem Tools هو أداة شاملة للمسلمين، يقدم مجموعة من الميزات التي تلبي احتياجاتهم اليومية في العبادة والتعلم. يوفر البرنامج تجربة مريحة وسهلة الاستخدام مع أدوات متنوعة لتحسين حياتك الدينية.\n\nميزات برنامج Moslem Tools\n\n1. قراءة واستماع للقرآن الكريم\nقراءة القرآن الكريم بالتقسيمات المختلفة (سور، صفحات، أجزاء، أرباع، وأحزاب).\nالاستماع للقرآن الكريم بعدة أصوات لمجموعة كبيرة من القراء.\nإمكانية تحميل القراء للاستماع بدون الحاجة إلى الإنترنت.\nتوفر الترجمات والتفاسير للقرآن الكريم، قابلة للتنزيل والاستخدام.\nإعراب الآيات أو السور المحددة.\nالبحث السهل في القرآن الكريم.\n\n2. الأذكار\nقراءة أذكار الصباح والمساء وغيرها من الأذكار اليومية.\nإمكانية إرسال إشعارات تحتوي على ذكر صوتي أو كتابي بشكل عشوائي حسب المدة المحددة.\n\n3. السبحة الإلكترونية\nعداد إلكتروني للأذكار ليس له حدود للعد.\n\n4. محول التاريخ\nتحويل التاريخ من هجري إلى ميلادي والعكس بسهولة.\n\n5. معاني أسماء الله الحسنى\nاستعراض معاني أسماء الله الحسنى الموجودة في الأحاديث الصحيحة.\n\n6. الأحاديث الصحيحة\nقراءة وتحميل كتب الأحاديث الصحيحة.\nالبحث السهل في الأحاديث.\n\n7. الراديو الإسلامي\nاستماع إلى محطات إذاعية إسلامية تتعلق بالقرآن الكريم، التفسير، والعلوم الدينية.\n\n8. وضع العلامات المرجعية\nوضع علامات مرجعية للعودة إلى مكان القراءة سواء في القرآن أو الأحاديث.\n\n9. عرض مواقيت الصلاة والتاريخ الميلادي والهجري\nيعرض البرنامج مواقيت الصلاة والتاريخ الميلادي والهجري لليوم الحالي.\n\nاختصارات لوحة المفاتيح في Moslem Tools\n\nإعادة تحميل مواقيت الصلاة F5\n\nالتحكم في السبحة الإلكترونية\nCTRL + S: قراءة الرقم الحالي للسبحة لمستخدمي قارئ الشاشة.\n\nنسخ وتنسيق النصوص\nCTRL + A: نسخ كل النص.\nCTRL + C: نسخ النص المحدد.\nCTRL + S: الحفظ كملف نصي.\nCTRL + P: طباعة النص.\nCTRL + =: تكبير النص.\nCTRL + -: تصغير النص.\n\nالتحكم في القراءة والتشغيل\nزر المسافة (Space): تشغيل، إيقاف، أو إيقاف مؤقت.\nALT + السهم الأيمن: الانتقال إلى الذكر التالي، الآية التالية، أو الحديث التالي.\nALT + السهم الأيسر: العودة إلى الذكر السابق، الآية السابقة، أو الحديث السابق.\nCTRL + G: الانتقال مباشرة إلى آية أو حديث.\n\nالعلامات المرجعية\nزر الحذف (Delete): حذف العلامة المرجعية المحددة.\n\nتشغيل الإذاعات الإسلامية\nزر الإدخال (Enter): تشغيل أو إيقاف الإذاعة الحالية.\n\nاختصارات التحكم في المقطع للقرآن\nزر المسافة: تشغيل/إيقاف مؤقت\nإيقاف: CTRL + S\nفتح قائمة تنزيل السور: CTRLD\nالتقديم السريع لمدة 5 ثواني: ALT + السهم الأيمن\nالترجيع السريع لمدة 5 ثواني: ALT + السهم الأيسر\nالتقديم السريع لمدة 10 ثواني: ALT + السهم الأعلى\nالترجيع السريع لمدة 10 ثواني: ALT + السهم الأسفل\nالتقديم السريع لمدة 30 ثانية: CTRL + السهم الأيمن\nالترجيع السريع لمدة 30 ثانية: CTRL + السهم الأيسر\nالتقديم السريع لمدة دقيقة: CTRL + السهم الأعلى\nالترجيع السريع لمدة دقيقة: CTRL + السهم الأسفل\nاختصارات Ctrl + الرقم للانتقال مباشرة إلى نسبة محددة من المقطع، على سبيل المثال، Ctrl + 1 للانتقال إلى 10% من المقطع، Ctrl + 2 للانتقال إلى 20%، وهكذا\nرفع الصوت: SHIFT + السهم الأعلى\nخفض الصوت: SHIFT + السهم الأسفل\n\nالمطورين\nعبد الرحمن محمد، أنس محمد.\n\nالخاتمة\nبرنامج Moslem Tools هو رفيقك اليومي لتعزيز تجربتك الدينية، سواء كنت تقرأ القرآن، تستمع للأذكار، أو تبحث في الأحاديث. مع هذه الميزات المتنوعة والاختصارات العملية، ستجد البرنامج سهلاً ومفيداً."))
        self.guide.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.guide.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.guide.setFont(font)        
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setText(str(self.font_size))
        layout=qt.QVBoxLayout(self)        
        layout.addWidget(self.guide)        
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        text_options=qt.QMenu(_("خيارات النص"),self)
        save=text_options.addAction(_("حفظ كملف نصي"))
        save.triggered.connect(self.save_text_as_txt)        
        print=text_options.addAction(_("طباعة"))
        print.triggered.connect(self.print_text)
        copy_all=text_options.addAction(_("نسخ النص كاملا"))        
        copy_all.triggered.connect(self.copy_text)
        copy_selected_text=text_options.addAction(_("نسخ النص المحدد"))
        copy_selected_text.triggered.connect(self.copy_line)
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)        
        menu.addMenu(text_options)
        menu.addMenu(fontMenu)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def print_text(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.guide.print(printer)
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
                    text = self.guide.toPlainText()
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
        cursor=self.guide.textCursor()
        self.guide.selectAll()
        font=self.guide.font()
        font.setPointSize(self.font_size)
        self.guide.setCurrentFont(font)        
        self.guide.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.guide.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.guide.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))