import guiTools,os,json
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
path=os.path.join(os.getenv('appdata'),app.appName,"athkar.json")
if not os.path.exists(path):
    with open(path,"w",encoding="utf-8") as file:
        file.write("[]")
class sibha(qt.QWidget):
    def __init__(self):
        super().__init__()        
        qt1.QShortcut("ctrl+s", self).activated.connect(self.speak_number)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.speak_current_thecre)                
        with open(path,"r",encoding="utf-8") as file:
            self.externalAthkar=json.load(file)
        self.athkar_laybol = qt.QLabel(_("قم بتحديد الذكر"))
        self.athkar_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)                
        self.athkar = qt.QComboBox()        
        self.athkar.setAccessibleDescription(_("control plus c لنطق الذكر المحدد"))
        self.athkar.setAccessibleName(_("قم بتحديد الذكر"))
        self.athkar.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.athkar.customContextMenuRequested.connect(self.onDelete)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
        self.athkar.addItems([
            _("سبحان الله"),
            _("الحمد لله "),
            _("لا إلاه إلا الله"),
            _("الله أكبر"),
            _("ربي اغفر لي"),
            _("أستغفر الله"),
            _("لا حول ولا قوة إلا بالله"),
            _("اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي"),
            _("اللهم صل وسلم وبارك على سيدنا محمد"),
            _("سبحان الله وبحمده سبحان الله العظيم"),
            _("اللَّهُمَّ ٱغْفِرْ لِي ذَنْبِي كُلَّهُ، دِقَّهُ وَجِلَّهُ، عَلَانِيَتَهُ وَسِرَّهُ، وَأَوَّلَهُ وَآخِرَهُ"),
            _("الله أكبر كبيرا والحمد لله كثيرا وسبحان الله بُكرةً وأصيلا"),
            _("سبحان الله والحمد لله ولا إلاه إلا الله والله أكبر"),
            _("أستغفر الله الذي لا إلاه إلا هو الحي القيوم وأتوب إليه"),
            _("لا إلاه إلا أنت سبحانك إني كنت من الظالمين"),
            _("سبحان الله وبحمده عدد خلقه ورضى نفسه وزنة عرشه ومداد كلماته"),
            _("لا إلاه إلا الله وحده لا شريك لهُ ، لهُ الملك ، ولهُ الحمدُ ، وهو على كل شيء قدير")
        ])        
        self.athkar.addItems(self.externalAthkar)
        self.numbers = qt.QLabel("0")
        self.numbers.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.numbers.setStyleSheet("font-size:300px;")        
        self.numbers.setFocusPolicy(qt2.Qt.FocusPolicy.StrongFocus)
        self.reset = qt.QPushButton(_("إعادة تعين"))
        self.reset.setAccessibleDescription("control plus R")
        self.reset.setDefault(True)
        self.reset.setShortcut("ctrl+r")
        self.reset.clicked.connect(self.reset_count)
        self.reset.setObjectName("resetButton")
        self.add = qt.QPushButton(_("التسبيح"))
        self.add.setAccessibleDescription("control plus equals")
        self.add.setShortcut("ctrl+=")
        self.add.setDefault(True)
        self.add.clicked.connect(self.increment_count)
        self.add.setObjectName("addButton")
        self.add_thecr=qt.QPushButton(_("إضافة ذكر"))
        self.add_thecr.setDefault(True)
        self.add_thecr.setAccessibleDescription("control plus a")
        self.add_thecr.setShortcut("ctrl+a")
        self.line_of_thecr=qt.QLineEdit()
        self.line_of_thecr.textChanged.connect(self.onLineTextChanged)
        self.line_of_thecr.setPlaceholderText(_("أكتب الذكر"))
        self.line_of_thecr.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.done_thecr=qt.QPushButton(_("إضافة الذكر"))
        self.done_thecr.setDefault(True)        
        self.done_thecr.clicked.connect(self.onAddThkarCompeleted)
        self.cancel_add=qt.QPushButton(_("إلغاء"))
        self.cancel_add.setDefault(True)
        self.cancel_add.setShortcut("shift+c")
        self.cancel_add.setAccessibleDescription("shift plus c")
        self.cancel_add.clicked.connect(self.cansel_add_thecr)
        self.cancel_add.setStyleSheet("""
            background-color: #8B0000;
            color: white;
        """)
        self.line_of_thecr.setVisible(False)
        self.done_thecr.setVisible(False)
        self.cancel_add.setVisible(False)
        self.add_thecr.clicked.connect(self.onAddThakar)
        self.add_thecr.setStyleSheet("""
            background-color: green;
            color: white;
        """)
        self.done_thecr.setStyleSheet("""
            background-color: green;
            color: white;
        """)
        main_layout = qt.QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)        
        layout1=qt.QHBoxLayout()
        layout1.addWidget(self.athkar_laybol)
        layout1.addWidget(self.athkar)
        layout1.addWidget(self.add_thecr)
        layout2=qt.QHBoxLayout()
        layout2.addWidget(self.cancel_add)
        layout2.addWidget(self.line_of_thecr)
        layout2.addWidget(self.done_thecr)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addWidget(self.numbers)
        btn_layout = qt.QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.addWidget(self.reset)
        btn_layout.addWidget(self.add)
        main_layout.addLayout(btn_layout)        
        self.setLayout(main_layout)
        self.setStyleSheet("""
            QPushButton#resetButton {
                background-color: #8B0000;
                color: white;
                min-height: 40px;
                font-size: 16px;
            }
            QPushButton#addButton {
                background-color: green;
                color: white;
                min-height: 40px;
                font-size: 16px;
            }
            QComboBox, QLineEdit {
                min-height: 40px;
                font-size: 16px;
            }
            QLabel {
                font-size: 16px;
            }
        """)
    def cansel_add_thecr(self):
        self.add_thecr.setVisible(True)
        self.line_of_thecr.setVisible(False)
        self.done_thecr.setVisible(False)
        self.cancel_add.setVisible(False)
        self.line_of_thecr.clear()
    def reset_count(self):
        self.numbers.setText("0")
        guiTools.speak(_("تم إعادة التعيين الى 0"))
    def increment_count(self):
        current_count = int(self.numbers.text())
        current_count += 1
        self.numbers.setText(str(current_count))
        guiTools.speak(str(current_count))
    def speak_number(self):
        current_number = self.numbers.text()
        guiTools.speak(current_number)
    def speak_current_thecre(self):
        guiTools.speak(self.athkar.currentText())
    def onAddThakar(self):
        self.add_thecr.setVisible(False)
        self.line_of_thecr.setVisible(True)
        self.done_thecr.setVisible(True)
        self.cancel_add.setVisible(True)
        self.done_thecr.setDisabled(True)
        self.line_of_thecr.setFocus()
    def onAddThkarCompeleted(self):
        thkar=self.line_of_thecr.text()
        self.line_of_thecr.setText("")
        self.externalAthkar.append(thkar)
        self.athkar.addItem(thkar)
        with open(path,"w",encoding="utf-8") as file:
            json.dump(self.externalAthkar,file,ensure_ascii=False,indent=4)
        self.add_thecr.setVisible(True)
        self.line_of_thecr.setVisible(False)
        self.done_thecr.setVisible(False)
        self.athkar.setFocus()
    def onLineTextChanged(self,text):
        if text=="":
            disabled=True
        else:
            disabled=False
        self.done_thecr.setDisabled(disabled)
    def onDelete(self):
        itemText=self.athkar.currentText()
        if not itemText in self.externalAthkar:
            qt.QMessageBox.critical(self,_("تنبيه"),_("لا يمكنك حذف هذا الذكر"))
        else:
            question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف هذا الذكر"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
            if question==qt.QMessageBox.StandardButton.Yes:
                self.externalAthkar.remove(itemText)
                self.athkar.removeItem(self.athkar.currentIndex())
                with open(path,"w",encoding="utf-8") as file:
                    json.dump(self.externalAthkar,file,ensure_ascii=False,indent=4)
                guiTools.speak(_("تم الحذف"))