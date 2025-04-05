import gui.translationViewer
import gui,guiTools,functions,re
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class Quran(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.infoData=[]
        layout=qt.QVBoxLayout(self)
        self.serch=qt.QLabel(_("بحث"))
        self.serch.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)        
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        self.search_bar.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)        
        self.by=qt.QLabel(_("التصفح ب"))
        self.by.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.by)        
        self.type=qt.QComboBox()
        self.type.setAccessibleName(_("التصفح ب"))
        self.type.addItems([_("سور"), _("صفحات"), _("أجزاء"), _("أرباع"), _("أحزاب")])
        self.type.currentIndexChanged.connect(self.onTypeChanged)                        
        self.custom=guiTools.QPushButton(_("مخصص"))        
        self.custom.clicked.connect(lambda: self.fromToSuraah.exec())
        layout.addWidget(self.type)        
        layout.addWidget(self.custom)
        layout.addWidget(self.serch)
        layout.addWidget(self.search_bar)
        self.info=guiTools.QListWidget()
        self.info.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.info.customContextMenuRequested.connect(self.onContextMenu)
        self.info.itemActivated.connect(self.onItemTriggered)
        self.info1=qt.QLineEdit()
        self.info1.setReadOnly(True)
        self.info1.setText(_("لخيارات عنصر الفئة, نستخدم مفتاح التطبيقات أو clic الأيمن"))
        self.info1.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.user_guide=qt.QPushButton(_("دليل الاختصارات"))
        self.user_guide.setDefault(True)
        self.user_guide.setShortcut("ctrl+f1")
        self.user_guide.setAccessibleDescription(_("control plus f1"))
        self.user_guide.clicked.connect(lambda: guiTools.TextViewer(self,_("دليل الاختصارات"),_("اختصارات الآية الحالية\nspace: تشغيل الآية\nctrl+t: تفسير الآية الحالية\nctrl+i: إعراب الآية الحالية\nctrl+r: أسباب نزول الآية الحالية\nctrl+l: ترجمة الآية الحالية\nctrl+f: معلومات الآية الحالية\nctrl+b: إضافة علامة مرجعية\nاختصارات الفئة\nctrl+a: نسخ الفئة\nctrl+s: حفظ الفئة كملف نصي\nctrl+p: طباعة الفئة\nctrl+shift+t: تفسير الفئة\nctrl+shift+i: إعراب الفئة\nctrl+shift+f: معلومات السورة\nctrl+shift+l: ترجمة  الفئة\nctrl+shift+p: التشغيل إلى نهاية الفئة\nctrl+alt+t: التفسير من آية إلى آية\nctrl+alt+l: الترجمة من آية إلى آية\nctrl+alt+i: الإعراب من آية إلى آية\nctrl+alt+p: التشغيل من آية إلى آية\nاختصارات حجم الخط\nctrl+=: تكبير الخط\nctrl+-: تصغير الخط\nاختصارات التنقل\nalt زائد السهم الأيسر: الفئة السابقة\nalt زائد السهم الأيمن: الفئة التالية\nctrl+shift+g:الذهاب إلى محتوى فئة\nctrl+f1: دليل الاختصارات")).exec())
        layout.addWidget(self.info)                
        layout.addWidget(self.info1)
        layout.addWidget(self.user_guide)
        self.fromToSuraah=guiTools.FromToSurahWidget(self)        
        self.onTypeChanged(0)
    def search(self,pattern,text_list):    
        tashkeel_pattern=re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670]')        
        normalized_pattern=tashkeel_pattern.sub('', pattern)        
        matches=[
            text for text in text_list
            if normalized_pattern in tashkeel_pattern.sub('', text)
        ]        
        return matches        
    def onsearch(self):
        search_text=self.search_bar.text().lower()
        self.info.clear()
        result=self.search(search_text,self.infoData)
        self.info.addItems(result)
    def onItemTriggered(self):
        index=self.type.currentIndex()
        if index==0:
            result=functions.quranJsonControl.getSurahs()
        elif index==1:
            result=functions.quranJsonControl.getPage()
        elif index==2:
            result=functions.quranJsonControl.getJuz()
        elif index==3:
            result=functions.quranJsonControl.getHezb()
        elif index==4:
            result=functions.quranJsonControl.getHizb()
        gui.QuranViewer(self,result[self.info.currentItem().text()][1],index,self.info.currentItem().text(),enableNextPreviouseButtons=True,typeResult=result,CurrentIndex=self.info.currentRow()).exec()
    def onTypeChanged(self,index:int):
        state=True
        self.info.clear()
        self.infoData=[]
        if index==0:
            self.infoData=functions.quranJsonControl.getSurahs().keys()
        elif index==1:
            for i in range(1,605):
                self.infoData.append(str(i))
        elif index==2:
            for i in range(1,31):
                self.infoData.append(str(i))
        elif index==3:
            for i in range(1,241):
                self.infoData.append(str(i))
        elif index==4:
            for  i in range(1,61):
                self.infoData.append(str(i))                        
        self.info.addItems(self.infoData)
    def getResult(self):
        index=self.type.currentIndex()
        if index==0:
            result=functions.quranJsonControl.getSurahs()
        elif index==1:
            result=functions.quranJsonControl.getPage()
        elif index==2:
            result=functions.quranJsonControl.getJuz()
        elif index==3:
            result=functions.quranJsonControl.getHezb()
        elif index==4:
            result=functions.quranJsonControl.getHizb()
        return result[self.info.currentItem().text()][1]
    def onContextMenu(self):
        menu=qt.QMenu(self)
        menu.setFocus()
        listenAction=qt1.QAction(_("تشغيل"),self)
        menu.addAction(listenAction)
        listenAction.triggered.connect(self.onListenActionTriggert)
        menu.setDefaultAction(listenAction)
        tafseerAction=qt1.QAction(_("تفسير"),self)
        menu.addAction(tafseerAction)
        tafseerAction.triggered.connect(self.onTafseerActionTriggered)
        translationAction=qt1.QAction(_("ترجمة"),self)
        menu.addAction(translationAction)
        translationAction.triggered.connect(self.onTranslationActionTriggered)
        iarabAction=qt1.QAction(_("إعراب"),self)
        menu.addAction(iarabAction)
        iarabAction.triggered.connect(self.onIarabActionTriggered)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def onListenActionTriggert(self):
        result=self.getResult()
        gui.QuranPlayer(self,result,0,self.type.currentIndex(),self.info.currentItem().text(),enableBookMarks=True).exec()
    def onTafseerActionTriggered(self):
        ayahList=self.getResult().split("\n")
        Ayah,surah,juz,page,AyahNumber1=functions.quranJsonControl.getAyah(ayahList[0])
        Ayah,surah,juz,page,AyahNumber2=functions.quranJsonControl.getAyah(ayahList[-1])
        gui.TafaseerViewer(self,AyahNumber1,AyahNumber2).exec()
    def onTranslationActionTriggered(self):
        ayahList=self.getResult().split("\n")
        Ayah,surah,juz,page,AyahNumber1=functions.quranJsonControl.getAyah(ayahList[0])
        Ayah,surah,juz,page,AyahNumber2=functions.quranJsonControl.getAyah(ayahList[-1])
        gui.translationViewer(self,AyahNumber1,AyahNumber2).exec()
    def onIarabActionTriggered(self):
        ayahList=self.getResult().split("\n")
        Ayah,surah,juz,page,AyahNumber1=functions.quranJsonControl.getAyah(ayahList[0])
        Ayah,surah,juz,page,AyahNumber2=functions.quranJsonControl.getAyah(ayahList[-1])
        result=functions.iarab.getIarab(AyahNumber1,AyahNumber2)
        guiTools.TextViewer(self,_("إعراب"),result).exec()