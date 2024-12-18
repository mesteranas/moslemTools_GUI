from PyQt6 import QtWidgets as qt
from PyQt6 import QtCore as qt2
class AfterAdaan(qt.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(1200,600)
        self.setWindowTitle(_("دعاء بعد الأذان"))        
        self.suplication=qt.QTextEdit()
        self.suplication.setReadOnly(True)                                    
        self.suplication.setTextInteractionFlags(qt2.Qt.TextInteractionFlag.TextSelectableByMouse|qt2.Qt.TextInteractionFlag.TextSelectableByKeyboard)        
        self.suplication.setLineWrapMode(qt.QTextEdit.LineWrapMode.NoWrap)
        self.suplication.setAcceptRichText(True)
        self.suplication.setAccessibleName(_("دعاء بعد الأذان"))
        self.suplication.setText(_("اللَّهُمَّ رَبَّ هَذِهِ الدَّعْوَةِ التَّامَّةِ، وَالصَّلَاةِ القَائِمَةِ، آتِ مُحَمَّدًا الوَسِيلَةَ وَالفَضِيلَةَ، وَابْعَثْهُ مَقَامًا مَحْمُودًا الَّذِي وَعَدْتَهُ\nيُستحب إضافة: إِنَّكَ لَا تُخْلِفُ المِيعَادَ.\n\nثواب الدعاء بعد الأذان\nقال رسول الله صل الله عليه وسلم: مَنْ قَالَ حِينَ يَسْمَعُ النِّدَاءَ: اللَّهُمَّ رَبَّ هَذِهِ الدَّعْوَةِ التَّامَّةِ، وَالصَّلَاةِ القَائِمَةِ، آتِ مُحَمَّدًا الوَسِيلَةَ وَالفَضِيلَةَ، وَابْعَثْهُ مَقَامًا مَحْمُودًا الَّذِي وَعَدْتَهُ؛ حَلَّتْ لَهُ شَفَاعَتِي يَوْمَ القِيَامَةِ\nرواه البخاري في صحيحه."))
        layout=qt.QVBoxLayout()
        layout.addWidget(self.suplication)
        self.setLayout(layout)