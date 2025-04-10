import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class sibha(qt.QWidget):
    def __init__(self):
        super().__init__()        
        qt1.QShortcut("ctrl+s", self).activated.connect(self.speak_number)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.speak_current_thecre)                
        self.athkar_laybol = qt.QLabel(_("قم بتحديد الذكر"))
        self.athkar_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)                
        self.athkar = qt.QComboBox()        
        self.athkar.setAccessibleDescription(_("control plus c لنطق الذكر المحدد"))
        self.athkar.setAccessibleName(_("قم بتحديد الذكر"))
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
        self.numbers = qt.QLabel("0")
        self.numbers.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.numbers.setStyleSheet("font-size:300px;")        
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
        main_layout = qt.QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)        
        main_layout.addWidget(self.athkar_laybol)
        main_layout.addWidget(self.athkar)
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