import functions, gui, guiTools
import PyQt6.QtWidgets as qt
class FromToSurahWidget(qt.QDialog):
    def __init__(self, p):
        super().__init__()
        self.p = p
        self.resize(300,200)
        self.surahs = functions.quranJsonControl.getSurahs()                
        self.label_from_surah = qt.QLabel(_("من سورة"))
        self.combo_from_surah = qt.QComboBox()
        self.combo_from_surah.addItems(self.surahs)        
        self.combo_from_surah.setAccessibleName(_("من سورة"))
        self.label_from_verse = qt.QLabel(_("من الآية"))
        self.spin_from_verse = qt.QSpinBox()        
        self.spin_from_verse.setAccessibleName(_("من الآية"))
        self.label_to_surah = qt.QLabel(_("الى سورة"))
        self.combo_to_surah = qt.QComboBox()
        self.combo_to_surah.setAccessibleName(_("الى سورة"))
        self.combo_to_surah.addItems(self.surahs)        
        self.label_to_verse = qt.QLabel(_("الى الآية"))
        self.spin_to_verse = qt.QSpinBox()        
        self.spin_to_verse.setAccessibleName(_("الى الآية"))
        self.go = qt.QPushButton(_("الذهاب"))                                   
        self.go.setStyleSheet("""
    QPushButton {
        background-color: #1e7e34;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #19692c;
    }
""")
        h_layout1 = qt.QHBoxLayout()
        h_layout1.addWidget(self.label_from_surah)
        h_layout1.addWidget(self.combo_from_surah)        
        h_layout2 = qt.QHBoxLayout()
        h_layout2.addWidget(self.label_from_verse)
        h_layout2.addWidget(self.spin_from_verse)        
        h_layout3 = qt.QHBoxLayout()
        h_layout3.addWidget(self.label_to_surah)
        h_layout3.addWidget(self.combo_to_surah)        
        h_layout4 = qt.QHBoxLayout()
        h_layout4.addWidget(self.label_to_verse)
        h_layout4.addWidget(self.spin_to_verse)                
        main_layout = qt.QVBoxLayout()
        main_layout.addLayout(h_layout1)
        main_layout.addLayout(h_layout2)
        main_layout.addLayout(h_layout3)
        main_layout.addLayout(h_layout4)
        main_layout.addWidget(self.go)        
        self.setLayout(main_layout)                
        self.combo_from_surah.currentIndexChanged.connect(self.handle_surah_change)
        self.combo_to_surah.currentIndexChanged.connect(self.handle_to_surah_change)
        self.spin_from_verse.valueChanged.connect(self.handle_verse_change)
        self.spin_to_verse.valueChanged.connect(self.handle_verse_change)
        self.go.clicked.connect(self.onGo)        
        self.handle_surah_change()        
    def handle_surah_change(self):        
        if self.combo_to_surah.currentIndex() < self.combo_from_surah.currentIndex():
            self.combo_to_surah.setCurrentIndex(self.combo_from_surah.currentIndex())        
        surah_from_text = self.combo_from_surah.currentText()
        surah_to_text = self.combo_to_surah.currentText()
        num_verses_from = len(self.surahs[surah_from_text][1].split("\n"))
        num_verses_to = len(self.surahs[surah_to_text][1].split("\n"))
        self.spin_from_verse.setRange(1, num_verses_from)
        self.spin_from_verse.setValue(1)
        self.spin_to_verse.setRange(1, num_verses_to)
        self.spin_to_verse.setValue(num_verses_to)
        self.handle_verse_change()    
    def handle_verse_change(self):        
        if self.combo_from_surah.currentIndex() == self.combo_to_surah.currentIndex():
            if self.spin_to_verse.value() <= self.spin_from_verse.value():
                self.spin_to_verse.setValue(len(self.surahs[self.combo_to_surah.currentText()][1].split("\n")))    
    def onGo(self):
        result = functions.quranJsonControl.getFromTo(
            self.combo_from_surah.currentIndex() + 1,
            self.spin_from_verse.value(),
            self.combo_to_surah.currentIndex() + 1,
            self.spin_to_verse.value()
        )
        gui.QuranViewer(self.p, "\n".join(result), 5, 0, enableBookmarks=False).exec()
    def handle_to_surah_change(self):        
        if self.combo_to_surah.currentIndex() < self.combo_from_surah.currentIndex():
            self.combo_to_surah.setCurrentIndex(self.combo_from_surah.currentIndex())        
        surah_from_text = self.combo_from_surah.currentText()
        surah_to_text = self.combo_to_surah.currentText()
        num_verses_to = len(self.surahs[surah_to_text][1].split("\n"))
        self.spin_to_verse.setRange(1, num_verses_to)
        self.spin_to_verse.setValue(num_verses_to)
        self.handle_verse_change()    