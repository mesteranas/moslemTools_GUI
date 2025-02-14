import guiTools,time
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
class other_brotcasts(qt.QWidget):
    def __init__(self):
        super().__init__()            
        self.list_of_other=qt.QListWidget()
        self.list_of_other.itemActivated.connect(self.play)
        self.list_of_other.addItem(_("تَكْبِيرَات العيد"))
        self.list_of_other.addItem(_("الرقية الشرعية"))        
        self.list_of_other.addItem(_("إذاعة الصحابة"))
        self.list_of_other.addItem(_("فتاوى إبن باز"))
        self.list_of_other.addItem(_("صور من حياة الصحابة"))
        self.list_of_other.addItem(_("إذاعة عمر عبد الكافي"))
        self.list_of_other.addItem(_("السُنَّة السلفية"))
        self.list_of_other.addItem(_("في ظِلال السيرة النبوية"))
        self.list_of_other.addItem(_("فتاوى ابن العُثيمين"))
        self.list_of_other.addItem(_("العاصمة أونلاين"))        
        self.list_of_other.addItem(_("الإحسان"))        
        self.list_of_other.addItem(_("الإستقامى"))
        self.list_of_other.addItem(_("الفتح"))        
        self.list_of_other.addItem(_("المرأة المسلمة"))
        self.list_of_other.addItem(_("اللغة العربية وعلومها"))
        self.list_of_other.addItem(_("المهارات الحياتية والعلوم التربوية"))
        self.list_of_other.addItem(_("السلوك والآداب والأخلاق ومحاسن الأعمال"))
        self.list_of_other.addItem(_("التوعية الاجتماعية"))
        self.list_of_other.addItem(_("الإذاعة الفقهية"))
        self.list_of_other.addItem(_("الحج"))
        self.list_of_other.addItem(_("رمضان المبارك"))
        self.list_of_other.addItem(_("التراجم والتاريخ والسير"))
        self.list_of_other.addItem(_("الفكر والدعوة والثقافة الإسلامية"))
        self.list_of_other.addItem(_("السيرة النبوية وقصص القرآن والأنبياء والصحابة"))
        self.list_of_other.addItem(_("الحديث وعلومه"))
        self.list_of_other.addItem(_("العقيدة والتوحيد"))
        self.list_of_other.addItem(_("علوم القرآن الكريم"))
        self.list_of_other.addItem(_("راديو كبار العلماء"))
        self.list_of_other.addItem(_("الدكتور سعد الحميد"))
        self.list_of_other.addItem(_("الدكتور خالد الجريسي"))    
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_other)    
        self.player=QMediaPlayer()
        self.audio=QAudioOutput()
        self.player.setAudioOutput(self.audio)
    def play(self):
        selected_item=self.list_of_other.currentItem()
        if not selected_item:
            return
        station_name=selected_item.text()
        if self.player.isPlaying():
            self.player.stop()
            return
        url=None
        if station_name == _("تَكْبِيرَات العيد"):
            url=qt2.QUrl("http://live.mp3quran.net:9728")
        elif station_name == _("الرقية الشرعية"):
            url=qt2.QUrl("http://live.mp3quran.net:9936")        
        elif station_name == _("إذاعة الصحابة"):
            url=qt2.QUrl("http://s5.voscast.com:10130/;stream1603343063302/1")
        elif station_name == _("فتاوى إبن باز"):
            url=qt2.QUrl("https://qurango.net/radio/alaikhtiarat_alfiqhayh_bin_baz")
        elif station_name == _("صور من حياة الصحابة"):
            url=qt2.QUrl("http://live.mp3quran.net:8028")
        elif station_name == _("إذاعة عمر عبد الكافي"):
            url=qt2.QUrl("http://node-28.zeno.fm/66geh5zntp8uv?zs=u1rolhJRRS-k08Aw1jvY8Q&rj-tok=AAABgNAugTEAylkfGQGe4UQM-w&rj-ttl=5")
        elif station_name == _("السُنَّة السلفية"):
            url=qt2.QUrl("http://andromeda.shoutca.st:8189/live")
        elif station_name == _("في ظِلال السيرة النبوية"):
            url=qt2.QUrl("https://Qurango.net/radio/fi_zilal_alsiyra")
        elif station_name == _("فتاوى ابن العُثيمين"):
            url=qt2.QUrl("http://live.mp3quran.net:8014")
        elif station_name == _("العاصمة أونلاين"):
            url=qt2.QUrl("https://asima.out.airtime.pro/asima_a")        
        elif station_name == _("الإحسان"):
            url=qt2.QUrl("https://cdn.bmstudiopk.com/alehsaan/live/playlist.m3u8")        
        elif station_name == _("الإستقامى"):
            url=qt2.QUrl("https://jmc-live.ercdn.net/alistiqama/alistiqama.m3u8")
        elif station_name == _("الفتح"):
            url=qt2.QUrl("https://alfat7-q.com:5443/LiveApp/streams/986613792230697141226562.m3u8")        
        elif station_name == _("المرأة المسلمة"):
            url=qt2.QUrl("https://radio.alukah.net/almarah")
        elif station_name == _("اللغة العربية وعلومها"):
            url=qt2.QUrl("https://radio.alukah.net/arabiyyah")
        elif station_name == _("المهارات الحياتية والعلوم التربوية"):
            url=qt2.QUrl("https://radio.alukah.net/maharat")
        elif station_name == _("السلوك والآداب والأخلاق ومحاسن الأعمال"):
            url=qt2.QUrl("https://radio.alukah.net/assuluk")
        elif station_name == _("التوعية الاجتماعية"):
            url=qt2.QUrl("https://radio.alukah.net/attawiyy")
        elif station_name == _("الإذاعة الفقهية"):
            url=qt2.QUrl("https://radio.alukah.net/fiqhiyyah")
        elif station_name == _("الحج"):
            url=qt2.QUrl("https://radio.alukah.net/hajj")
        elif station_name == _("رمضان المبارك"):
            url=qt2.QUrl("https://radio.alukah.net/ramdan")
        elif station_name == _("التراجم والتاريخ والسير"):
            url=qt2.QUrl("https://radio.alukah.net/tarajim")
        elif station_name == _("الفكر والدعوة والثقافة الإسلامية"):
            url=qt2.QUrl("https://radio.alukah.net/alfikr")
        elif station_name == _("السيرة النبوية وقصص القرآن والأنبياء والصحابة"):
            url=qt2.QUrl("https://radio.alukah.net/sirah")
        elif station_name == _("الحديث وعلومه"):
            url=qt2.QUrl("https://radio.alukah.net/hadith")
        elif station_name == _("العقيدة والتوحيد"):
            url=qt2.QUrl("https://radio.alukah.net/aqidah")
        elif station_name == _("علوم القرآن الكريم"):
            url=qt2.QUrl("https://radio.alukah.net/ulumalquran")
        elif station_name == _("راديو كبار العلماء"):
            url=qt2.QUrl("https://radio.alukah.net/ulama")
        elif station_name == _("الدكتور سعد الحميد"):
            url=qt2.QUrl("https://radio.alukah.net/humayid")
        elif station_name == _("الدكتور خالد الجريسي"):
            url=qt2.QUrl("https://radio.alukah.net/aljeraisy")    
        if url:
            self.player.setSource(url)
            self.player.play()
class brotcasts_of_suplications(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_adhkar=qt.QListWidget()
        self.list_of_adhkar.itemActivated.connect(self.play)
        self.list_of_adhkar.addItem(_("اذكار الصباح"))
        self.list_of_adhkar.addItem(_("أذكار المساء"))
        self.list_of_adhkar.addItem(_("أدعية وأذكار يومية"))    
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_adhkar)    
        self.player=QMediaPlayer()
        self.audio=QAudioOutput()
        self.player.setAudioOutput(self.audio)    
    def play(self):
        selected_item=self.list_of_adhkar.currentItem()
        if not selected_item:
            return
        station_name=selected_item.text()
        if self.player.isPlaying():
            self.player.stop()
            return
        url=None
        if station_name == _("اذكار الصباح"):
            url=qt2.QUrl("https://qurango.net/radio/athkar_sabah")
        elif station_name == _("أذكار المساء"):
            url=qt2.QUrl("https://qurango.net/radio/athkar_masa")
        elif station_name == _("أدعية وأذكار يومية"):
            url=qt2.QUrl("https://radio.alukah.net/adiyyaha")
        if url:
            self.player.setSource(url)
            self.player.play()
class brotcasts_of_tafseer(qt.QWidget):
    def __init__(self):
        super().__init__()            
        self.list_of_tafseer=qt.QListWidget()
        self.list_of_tafseer.itemActivated.connect(self.play)
        self.list_of_tafseer.addItem(_("تفسير النابلسي"))
        self.list_of_tafseer.addItem(_("تفسير الشعراوي"))
        self.list_of_tafseer.addItem(_("الله أكبر لتفسير الشعراوي"))
        self.list_of_tafseer.addItem(_("المختصر في التفسير"))
        self.list_of_tafseer.addItem(_("إذاعة التفسير"))    
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_tafseer)    
        self.player=QMediaPlayer()
        self.audio=QAudioOutput()
        self.player.setAudioOutput(self.audio)    
    def play(self):
        selected_item=self.list_of_tafseer.currentItem()
        if not selected_item:
            return
        station_name=selected_item.text()
        if self.player.isPlaying():
            self.player.stop()
            return  # إيقاف التشغيل دون إعادة تشغيل
        url=None
        if station_name == _("تفسير النابلسي"):
            url=qt2.QUrl("http://206.72.199.179:9992/;stream.mp3")
        elif station_name == _("تفسير الشعراوي"):
            url=qt2.QUrl("http://206.72.199.180:9990/;")
        elif station_name == _("الله أكبر لتفسير الشعراوي"):
            url=qt2.QUrl("http://66.45.232.132:9996/;stream.mp3")
        elif station_name == _("المختصر في التفسير"):
            url=qt2.QUrl("http://live.mp3quran.net:9698")
        elif station_name == _("إذاعة التفسير"):
            url=qt2.QUrl("http://live.mp3quran.net:9718")
        if url:
            self.player.setSource(url)
            self.player.play()
class brotcasts_of_reciters(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_reciters=qt.QListWidget()
        self.list_of_reciters.itemActivated.connect(self.play)
        self.list_of_reciters.addItem(_("إذاعة القُراء"))
        self.list_of_reciters.addItem(_("القارء أبو بكر الشاطري"))
        self.list_of_reciters.addItem(_("القارئ إدريس أبكر"))
        self.list_of_reciters.addItem(_("القارئ سعود الشريم"))
        self.list_of_reciters.addItem(_("القارئ صلاح البدير"))
        self.list_of_reciters.addItem(_("القارئ عبد الباسط عبد الصمد"))
        self.list_of_reciters.addItem(_("القارئ عبد الرحمن السديس"))
        self.list_of_reciters.addItem(_("القارئ ماهر المعيقلي"))
        self.list_of_reciters.addItem(_("القارئ محمود خليل الحُصَري"))
        self.list_of_reciters.addItem(_("القارئ محمود خليل الحُصَري القرآن بالتحقيق"))
        self.list_of_reciters.addItem(_("القارئ محمود علي البنا القرآن بالتحقيق"))
        self.list_of_reciters.addItem(_("مشاري راشد"))
        self.list_of_reciters.addItem(_("القارئ مصطفى رعد العزاوي"))
        self.list_of_reciters.addItem(_("القارئ مصطفى اللاهونِي"))
        self.list_of_reciters.addItem(_("القارئ يحيى حوا"))
        self.list_of_reciters.addItem(_("القارئ يوسف بن نوح"))
        self.list_of_reciters.addItem(_("القارئ أحمد خضر الطرابلسي- رواية قالون عن نافع"))
        self.list_of_reciters.addItem(_("القارئ طارق دعوب- رواية قالون عن نافع"))
        self.list_of_reciters.addItem(_("القارئ عبد الباسط عبد الصمد- رواية ورش عن نافع"))
        self.list_of_reciters.addItem(_("القارئ محمد عبد الكريم رواية ورش عن نافع من طريق أبي بكر الأصبهاني"))
        self.list_of_reciters.addItem(_("القارئ  محمد عبد الحكيم قِراءة ابن كثير"))
        self.list_of_reciters.addItem(_("القارئ الفاتح محمد الزُبَيْري- رواية الدُوري عن أبي عمرو"))
        self.list_of_reciters.addItem(_("القارئ مفتاح السلطني- رواية الدُوري عن أبي عمرو"))    
        self.list_of_reciters.addItem(_("القارئ مفتاح السلطني- رواية ابن ذكوان عن ابن عامر"))
        self.list_of_reciters.addItem(_("القارئ محمد عبد الحكيم سعيد- رواية الدُوري عن الكِسائي"))
        self.list_of_reciters.addItem(_("القارئ عبد الرشيد صوفي- رواية خلف عن حمزة"))
        self.list_of_reciters.addItem(_("القارئ محمود الشيمي- رواية الدُوري عن الكِسائي"))
        self.list_of_reciters.addItem(_("القارئ مفتاح السلطني- رواية الدُوري عن الكِسائي"))
        self.list_of_reciters.addItem(_("القارئ ياسر المزروعي قِراءة يعقوب"))
        self.list_of_reciters.addItem(_("القارئ الشيخ العيون الكوشي - ورش عن نافع"))
        self.list_of_reciters.addItem(_("القارِء الشيخ سعد الغامدي"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_reciters)    
        self.player=QMediaPlayer()
        self.audio=QAudioOutput()
        self.player.setAudioOutput(self.audio)    
    def play(self):
        selected_item=self.list_of_reciters.currentItem()
        if not selected_item:
            return
        reciter_name=selected_item.text()    
        if self.player.isPlaying():
            self.player.stop()
            return
        url=None
        if reciter_name == _("إذاعة القُراء"):
            url=qt2.QUrl("http://live.mp3quran.net:8006")
        elif reciter_name == _("القارء أبو بكر الشاطري"):
            url=qt2.QUrl("http://live.mp3quran.net:9966")
        elif reciter_name == _("القارئ إدريس أبكر"):
            url=qt2.QUrl("http://live.mp3quran.net:9968")
        elif reciter_name == _("القارئ سعود الشريم"):
            url=qt2.QUrl("http://live.mp3quran.net:9986")
        elif reciter_name == _("القارئ صلاح البدير"):
            url=qt2.QUrl("https://qurango.net/radio/salah_albudair")
        elif reciter_name == _("القارئ عبد الباسط عبد الصمد"):
            url=qt2.QUrl("http://live.mp3quran.net:9980")
        elif reciter_name == _("القارئ عبد الرحمن السديس"):
            url=qt2.QUrl("http://live.mp3quran.net:9988")
        elif reciter_name == _("القارئ ماهر المعيقلي"):
            url=qt2.QUrl("http://live.mp3quran.net:9996")
        elif reciter_name == _("القارئ محمود خليل الحُصَري"):
            url=qt2.QUrl("http://live.mp3quran.net:9958/;")
        elif reciter_name == _("القارئ محمود خليل الحُصَري القرآن بالتحقيق"):
            url=qt2.QUrl("https://Qurango.net/radio/mahmoud_khalil_alhussary_mojawwad")
        elif reciter_name == _("القارئ محمود علي البنا القرآن بالتحقيق"):
            url=qt2.QUrl("https://qurango.net/radio/mahmoud_ali__albanna_mojawwad")
        elif reciter_name == _("مشاري راشد"):
            url=qt2.QUrl("http://live.mp3quran.net:9982")
        elif reciter_name == _("القارئ مصطفى رعد العزاوي"):
            url=qt2.QUrl("https://Qurango.net/radio/mustafa_raad_alazawy")
        elif reciter_name == _("القارئ مصطفى اللاهونِي"):
            url=qt2.QUrl("http://live.mp3quran.net:9798")
        elif reciter_name == _("القارئ يحيى حوا"):
            url=qt2.QUrl("https://Qurango.net/radio/yahya_hawwa")
        elif reciter_name == _("القارئ يوسف بن نوح"):
            url=qt2.QUrl("https://Qurango.net/radio/yousef_bin_noah_ahmad")
        elif reciter_name == _("القارئ أحمد خضر الطرابلسي- رواية قالون عن نافع"):
            url=qt2.QUrl("https://Qurango.net/radio/ahmad_khader_altarabulsi")
        elif reciter_name == _("القارئ طارق دعوب- رواية قالون عن نافع"):
            url=qt2.QUrl("https://qurango.net/radio/tareq_abdulgani_daawob")
        elif reciter_name == _("القارئ عبد الباسط عبد الصمد- رواية ورش عن نافع"):
            url=qt2.QUrl("http://live.mp3quran.net:9956")
        elif reciter_name == _("القارئ محمد عبد الكريم رواية ورش عن نافع من طريق أبي بكر الأصبهاني"):
            url=qt2.QUrl("https://qurango.net/radio/mohammad_abdullkarem_alasbahani")
        elif reciter_name == _("القارئ  محمد عبد الحكيم قِراءة ابن كثير"):
            url=qt2.QUrl("https://Qurango.net/radio/mohammad_alabdullah_albizi")
        elif reciter_name == _("القارئ الفاتح محمد الزُبَيْري- رواية الدُوري عن أبي عمرو"):
            url=qt2.QUrl("https://Qurango.net/radio/alfateh_alzubair")
        elif reciter_name == _("القارئ مفتاح السلطني- رواية الدُوري عن أبي عمرو"):
            url=qt2.QUrl("https://Qurango.net/radio/muftah_alsaltany_aldori_an_abi_amr")
        elif reciter_name == _("القارئ مفتاح السلطني- رواية ابن ذكوان عن ابن عامر"):
            url=qt2.QUrl("https://qurango.net/radio/muftah_alsaltany_ibn_thakwan_an_ibn_amr")
        elif reciter_name == _("القارئ محمد عبد الحكيم سعيد- رواية الدُوري عن الكِسائي"):
            url=qt2.QUrl("https://Qurango.net/radio/mohammad_alabdullah_aldorai")
        elif reciter_name == _("القارئ عبد الرشيد صوفي- رواية خلف عن حمزة"):
            url=qt2.QUrl("https://Qurango.net/radio/abdulrasheed_soufi_khalaf")
        elif reciter_name == _("القارئ محمود الشيمي- رواية الدُوري عن الكِسائي"):
            url=qt2.QUrl("https://Qurango.net/radio/mahmood_alsheimy")
        elif reciter_name == _("القارئ مفتاح السلطني- رواية الدُوري عن الكِسائي"):
            url=qt2.QUrl("https://Qurango.net/radio/muftah_alsaltany_aldorai")
        elif reciter_name == _("القارئ ياسر المزروعي قِراءة يعقوب"):
            url=qt2.QUrl("https://Qurango.net/radio/yasser_almazroyee")
        elif reciter_name == _("القارئ الشيخ العيون الكوشي - ورش عن نافع"):
            url=qt2.QUrl("http://live.mp3quran.net:9912/;")
        elif reciter_name == _("القارِء الشيخ سعد الغامدي"):
            url=qt2.QUrl("https://qurango.net/radio/saad_alghamdi")
        if url:
            self.player.setSource(url)
            self.player.play()        
class quran_brotcast(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_quran_brotcasts=qt.QListWidget()
        self.list_of_quran_brotcasts.itemActivated.connect(self.play)
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من نابلِس"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من القاهرة"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من السعودية"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من تونس"))        
        self.list_of_quran_brotcasts.addItem(_("إذاعة دُبَيْ للقرآن الكريم"))        
        self.list_of_quran_brotcasts.addItem(_("تلاوات خاشعة"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من أستراليا"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة طيبة للقرآن الكريم من السودان"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من مصر"))
        self.list_of_quran_brotcasts.addItem(_("إذاعة القرآن الكريم من فَلَسطين"))        
        self.list_of_quran_brotcasts.addItem(_("إذاعة تراتيل"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_quran_brotcasts)        
        self.player=QMediaPlayer()
        self.audio=QAudioOutput()
        self.player.setAudioOutput(self.audio)
    def play(self):
        selected_item=self.list_of_quran_brotcasts.currentItem()
        if not selected_item:
            return
        station_name=selected_item.text()
        if self.player.isPlaying():
            self.player.stop()
            return  # إيقاف التشغيل مباشرة دون إعادة تشغيل
        url=None
        if station_name == _("إذاعة القرآن الكريم من نابلِس"):
            url=qt2.QUrl("http://www.quran-radio.org:8002/;stream.mp3")
        elif station_name == _("إذاعة القرآن الكريم من القاهرة"):
            url=qt2.QUrl("http://n0e.radiojar.com/8s5u5tpdtwzuv?rj-ttl=5&rj-tok=AAABeel-l8gApvlPoJcG2WWz8A")
        elif station_name == _("إذاعة القرآن الكريم من السعودية"):            
            url=qt2.QUrl("https://stream.radiojar.com/4wqre23fytzuv")
        elif station_name == _("إذاعة القرآن الكريم من تونس"):              
            url=qt2.QUrl("http://5.135.194.225:8000/live")        
        elif station_name == _("إذاعة دُبَيْ للقرآن الكريم"):            
            url=qt2.QUrl("http://uk5.internet-radio.com:8079/stream")        
        elif station_name == _("تلاوات خاشعة"):
            url=qt2.QUrl("http://live.mp3quran.net:9992")
        elif station_name == _("إذاعة القرآن الكريم من أستراليا"):
            url=qt2.QUrl("http://listen.qkradio.com.au:8382/listen.mp3")
        elif station_name == _("إذاعة طيبة للقرآن الكريم من السودان"):
            url=qt2.QUrl("http://live.mp3quran.net:9960")
        elif station_name == _("إذاعة القرآن الكريم من مصر"):
            url= qt2.QUrl("http://66.45.232.131:9994/;stream")
        elif station_name == _("إذاعة القرآن الكريم من فَلَسطين"):
            url=qt2.QUrl("http://streamer.mada.ps:8029/quranfm")        
        elif station_name == _("إذاعة تراتيل"):
            url=qt2.QUrl("http://live.mp3quran.net:8030")
        if url:
            self.player.setSource(url)
            self.player.play()
class protcasts(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.brotcasts_tab=qt.QTabWidget()
        self.brotcasts_tab.addTab(quran_brotcast(), _("إذاعات القرآن الكريم"))
        self.brotcasts_tab.addTab(brotcasts_of_reciters(), _("إذاعات القراء"))
        self.brotcasts_tab.addTab(brotcasts_of_tafseer(), _("إذاعات التفاسير"))
        self.brotcasts_tab.addTab(brotcasts_of_suplications(), _("إذاعات الأذكار والأدعية"))
        self.brotcasts_tab.addTab(other_brotcasts(), _("إذاعات إسلامية أخرى"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.brotcasts_tab)