import functions,gui,guiTools
import PyQt6.QtWidgets as qt
class FromToSurahWidget(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        self.p=p
        self.setFixedSize(300, 200)
        self.surahs=functions.quranJsonControl.getSurahs()
        main_layout=qt.QVBoxLayout()
        
        self.group_from=qt.QGroupBox(_("من"))
        from_layout=qt.QFormLayout()
        self.from_suraah=qt.QComboBox()
        self.from_suraah.addItems(self.surahs)
        self.from_vers_spin=qt.QSpinBox()
        from_layout.addRow(_("السورة:"), self.from_suraah)
        from_layout.addRow(_("الآية:"), self.from_vers_spin)
        self.group_from.setLayout(from_layout)
        self.group_to=qt.QGroupBox(_("إلى"))
        to_layout=qt.QFormLayout()
        self.to_suraah=qt.QComboBox()
        self.to_suraah.addItems(self.surahs)
        self.to_vers_spin=qt.QSpinBox()
        to_layout.addRow(_("السورة:"), self.to_suraah)
        to_layout.addRow(_("الآية:"), self.to_vers_spin)
        self.group_to.setLayout(to_layout)
        
        main_layout.addWidget(self.group_from)
        main_layout.addWidget(self.group_to)
        self.go=guiTools.QPushButton(_("إذهب"))
        self.go.clicked.connect(self.onGo)
        to_layout.addWidget(self.go)
        self.setLayout(main_layout)
        
        self.from_suraah.currentIndexChanged.connect(self.handle_surah_change)
        self.to_suraah.currentIndexChanged.connect(self.handle_surah_change)
        self.from_vers_spin.valueChanged.connect(self.handle_verse_change)
        self.to_vers_spin.valueChanged.connect(self.handle_verse_change)
        self.handle_surah_change()
    def handle_surah_change(self):
        if self.to_suraah.currentIndex() < self.from_suraah.currentIndex():
            self.to_suraah.setCurrentIndex(self.from_suraah.currentIndex())
        self.from_vers_spin.setRange(1,len(self.surahs[self.from_suraah.currentText()][1].split("\n")))
        self.from_vers_spin.setValue(1)
        self.to_vers_spin.setRange(1,len(self.surahs[self.to_suraah.currentText()][1].split("\n")))
        self.to_vers_spin.setValue(len(self.surahs[self.to_suraah.currentText()][1].split("\n")))
        self.handle_verse_change()
    
    def handle_verse_change(self):
        if self.from_suraah.currentIndex() == self.to_suraah.currentIndex():
            if self.to_vers_spin.value() <= self.from_vers_spin.value():
                self.to_vers_spin.setValue(len(self.surahs[self.to_suraah.currentText()][1].split("\n")))

    def onGo(self):
        result=functions.quranJsonControl.getFromTo(self.from_suraah.currentIndex()+1,self.from_vers_spin.value(),self.to_suraah.currentIndex()+1,self.to_vers_spin.value())
        gui.QuranViewer(self.p,"\n".join(result),5,0,enableBookmarks=False).exec()