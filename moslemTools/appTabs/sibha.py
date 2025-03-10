import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class sibha(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("ctrl+s",self).activated.connect(self.speak_number)
        qt1.QShortcut("ctrl+c",self).activated.connect(self.speak_current_thecre)
        self.athkar_laybol=qt.QLabel(_("قم بتحديد الذكر"))
        self.athkar_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.athkar=qt.QComboBox()        
        self.athkar.setAccessibleDescription(_("control plus c لنطق الذكر المحدد"))
        self.athkar.setAccessibleName(_("قم بتحديد الذكر"))
        self.athkar.addItem(_("سبحان الله"))
        self.athkar.addItem(_("الحمد لله "))
        self.athkar.addItem(_("لا إلاه إلا الله"))
        self.athkar.addItem(_("الله أكبر"))
        self.athkar.addItem(_("ربي اغفر لي"))
        self.athkar.addItem(_("أستغفر الله"))
        self.athkar.addItem(_("لا حول ولا قوة إلا بالله"))
        self.athkar.addItem(_("اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي"))
        self.athkar.addItem(_("اللهم صل وسلم وبارك على سيدنا محمد"))
        self.athkar.addItem(_("سبحان الله وبحمده سبحان الله العظيم"))
        self.athkar.addItem(_("اللَّهُمَّ ٱغْفِرْ لِي ذَنْبِي كُلَّهُ، دِقَّهُ وَجِلَّهُ، عَلَانِيَتَهُ وَسِرَّهُ، وَأَوَّلَهُ وَآخِرَهُ"))
        self.athkar.addItem(_("الله أكبر كبيرا والحمد لله كثيرا وسبحان الله بُكرةً وأصيلا"))
        self.athkar.addItem(_("سبحان الله والحمد لله ولا إلاه إلا الله والله أكبر"))
        self.athkar.addItem(_("أستغفر الله الذي لا إلاه إلا هو الحي القيوم وأتوب إليه"))
        self.athkar.addItem(_("لا إلاه إلا أنت سبحانك إني كنت من الظالمين"))
        self.athkar.addItem(_("سبحان الله وبحمده عدد خلقه ورضى نفسه وزنة عرشه ومداد كلماته"))
        self.athkar.addItem(_("لا إلاه إلا الله وحده لا شريك لهُ ، لهُ الملك ، ولهُ الحمدُ ، وهو على كل شيء قدير"))
        self.reset=qt.QPushButton(_("إعادة تعين"))
        self.reset.setAccessibleDescription("control plus R")
        self.reset.setDefault(True)
        self.reset.setShortcut("ctrl+r")
        self.reset.clicked.connect(self.reset_count)
        self.numbers=qt.QLabel("0")
        self.numbers.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.numbers.setStyleSheet("font-size:300px;")
        self.add=qt.QPushButton(_("التسبيح"))
        self.add.setAccessibleDescription("control plus equals")
        self.add.setShortcut("ctrl+=")
        self.add.setDefault(True)
        self.add.clicked.connect(self.increment_count)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.athkar_laybol)
        layout.addWidget(self.athkar)
        layout.addWidget(self.reset)
        layout.addWidget(self.numbers)
        layout.addWidget(self.add)
        self.setLayout(layout)                
    def reset_count(self):
        self.numbers.setText("0")
        guiTools.speak(_("تم إعادة التعيين الى 0"))
    def increment_count(self):
        current_count=int(self.numbers.text())
        current_count += 1
        self.numbers.setText(str(current_count))
        guiTools.speak(str(current_count))
    def speak_number(self):
        current_number=self.numbers.text()
        guiTools.speak(current_number)
    def speak_current_thecre(self):
        guiTools.speak(self.athkar.currentText())