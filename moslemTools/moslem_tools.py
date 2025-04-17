import sys
from custome_errors import *
sys.excepthook = my_excepthook
import update, guiTools, json, random, os, shutil, datetime, webbrowser, requests, keyboard
from hijri_converter import Gregorian
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from appTabs import *
language.init_translation()
try:
    updatePath = os.path.join(os.getenv('appdata'), settings_handler.appName, "update")
    if os.path.exists(updatePath):
        shutil.rmtree(updatePath)
except:
    pass
class main(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("الإصدار:") + str(app.version))                
        guiTools.speak(_("مرحبا بك في moslem tools, جاري تشغيل البرنامج, الرجاء الانتظار."))
        keyboard.add_hotkey("alt+windows+p", self.random_audio_theker)
        self.resize(1100, 600)
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(int(settings_handler.get("athkar", "voiceVolume")) / 100)
        self.media_player.setAudioOutput(self.audio_output)
        self.timer = qt2.QTimer(self)
        self.timer.timeout.connect(self.random_audio_theker)
        layout = qt.QVBoxLayout()        
        self.date_of_publish=qt.QLineEdit()
        self.date_of_publish.setReadOnly(True)
        self.date_of_publish.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.date_of_publish.setText(_("تاريخ نشر البرنامج: 2 ديسمبر 2024,1 جُمادى الآخِرة 1446"))        
        self.info = qt.QLineEdit()
        self.info.setReadOnly(True)
        self.info.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout1=qt.QHBoxLayout()
        layout1.addWidget(self.info)
        layout2=qt.QVBoxLayout()        
        layout2.addWidget(self.date_of_publish)
        layout.addLayout(layout1)
        layout1.addLayout(layout2)
        self.viewInfoTextEdit()
        content_layout = qt.QHBoxLayout()
        self.list_widget = guiTools.listBook()        
        self.quranPlayer = QuranPlayer()
        self.storiesPlayer = StoryPlayer()
        tabs = [
            (prayer_times(), _("مواقيت الصلاة والتاريخ")),
            (Quran(), _("القرآن الكريم مكتوب")),
            (self.quranPlayer, _("القرآن الكريم صوتي")),
            (QuranRecitations(), _("قراءات القرآن الكريم")),
            (hadeeth(), _("الأحاديث النبوية والقدسية")),
            (IslamicBooks(), _("الكتب الإسلامية")),
            (ProphetStories(), _("القصص الإسلامية المكتوبة")),
            (self.storiesPlayer, _("القصص الإسلامية الصوتية")),
            (Albaheth(), _("الباحث في القرآن والأحاديث")),
            (protcasts(), _("الإذاعات الإسلامية")),
            (Athker(), _("الأذكار والأدعية")),
            (sibha(), _("سبحة إلكترونية")),
            (NamesOfAllah(), _("أسماء الله الحُسْنى")),
            (DateConverter(), _("محول التاريخ"))
        ]
        for widget_class, label in tabs:
            self.list_widget.add(label, widget_class)        
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            font = item.font()
            font.setBold(True)
            item.setFont(font)        
        fm = qt1.QFontMetrics(self.list_widget.font())
        max_width = 0
        for i in range(self.list_widget.count()):
            item_text = self.list_widget.item(i).text()
            text_width = fm.boundingRect(item_text).width()
            if text_width > max_width:
                max_width = text_width
        max_width += 40
        self.list_widget.setFixedWidth(max_width)        
        content_layout.addWidget(self.list_widget)
        content_layout.addWidget(self.list_widget.w, 1)
        layout.addLayout(content_layout)        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)        
        moreOptionsMenu = menubar.addMenu(_("المزيد من الخيارات"))
        action_settings = qt1.QAction(_("الإعدادات"), self)
        action_settings.setShortcut("f3")
        action_settings.triggered.connect(lambda: settings(self).exec())
        moreOptionsMenu.addAction(action_settings)
        action_bookMark = qt1.QAction(_("العلامات المرجعية"), self)
        action_bookMark.setShortcut("ctrl+b")
        action_bookMark.triggered.connect(lambda: book_marcks(self).exec())
        moreOptionsMenu.addAction(action_bookMark)
        action_whats_new = qt1.QAction(_("ما الجديد في هذا الإصدار"), self)
        action_whats_new.setShortcut("ctrl+w")
        action_whats_new.triggered.connect(self.whats_new_funktion)
        moreOptionsMenu.addAction(action_whats_new)
        action_license = qt1.QAction(_("الترخيص"), self)
        action_license.setShortcut("ctrl+l")
        action_license.triggered.connect(self.license_funktion)
        moreOptionsMenu.addAction(action_license)
        action_viewLastMessage = qt1.QAction(_("إظهار آخر رسالة من المطورين"), self)
        action_viewLastMessage.setShortcut("ctrl+m")
        action_viewLastMessage.triggered.connect(self.onViewLastMessageButtonClicked)
        moreOptionsMenu.addAction(action_viewLastMessage)
        action_user_guide = qt1.QAction(_("دليل المستخدم"), self)
        action_user_guide.setShortcut("f1")
        action_user_guide.triggered.connect(self.open_user_g_window)
        moreOptionsMenu.addAction(action_user_guide)
        action_about_devs = qt1.QAction(_("عن المطورين"), self)
        action_about_devs.setShortcut("f2")
        action_about_devs.triggered.connect(self.open_developers_window)
        moreOptionsMenu.addAction(action_about_devs)
        w = qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.tray_icon = qt.QSystemTrayIcon(self)
        self.tray_icon.setIcon(qt1.QIcon("data/icons/tray_icon.jpg"))
        self.tray_icon.setToolTip(app.name)
        self.tray_menu = qt.QMenu(self)
        self.random_thecker_audio = qt1.QAction(_("تشغيل ذكر عشوائي"))
        self.random_thecker_audio.triggered.connect(self.random_audio_theker)
        self.random_thecker_text = qt1.QAction(_("عرض ذكر عشوائي"))
        self.random_thecker_text.triggered.connect(self.show_random_theker)
        self.show_action = qt1.QAction(_("إخفاء البرنامج"))
        self.show_action.triggered.connect(self.toggle_visibility)
        self.close_action = qt1.QAction(_("إغلاق البرنامج"))
        self.close_action.triggered.connect(lambda: qt.QApplication.quit())
        self.tray_menu.addAction(self.random_thecker_audio)
        self.tray_menu.addAction(self.random_thecker_text)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.close_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        self.TIMER1 = qt2.QTimer(self)
        self.TIMER1.timeout.connect(self.show_random_theker)
        self.runAudioThkarTimer()
        self.notification_random_thecker()        
        guiTools.messageHandler.check(self)
        if settings_handler.get("update", "autoCheck") == "True":
            update.check(self, message=False)
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            self.show_action.setText(_("إظهار البرنامج"))
        else:
            self.show()
            self.show_action.setText(_("إخفاء البرنامج"))
    def show_random_theker(self):
        with open("data/json/text_athkar.json", "r", encoding="utf_8") as f:
            data = json.load(f)
        random_theckr = random.choice(data)
        guiTools.SendNotification(_("ذكر عشوائي"), random_theckr)
    def notification_random_thecker(self):
        self.TIMER1.stop()
        if formatDuration("athkar", "text") != 0:
            self.TIMER1.start(formatDuration("athkar", "text"))
    def runAudioThkarTimer(self):
        self.timer.stop()
        if formatDuration("athkar", "voice") != 0:
            self.timer.start(formatDuration("athkar", "voice"))
    def closeEvent(self, event):
        if app.exit:
            if settings_handler.get("g", "exitDialog") == "True":
                m = guiTools.ExitApp(self)
                m.exec()
                if m:
                    event.ignore()
            else:
                self.close()
        else:
            self.close()
    def random_audio_theker(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
            return
        folder_path = r"data\sounds\athkar"
        sound_files = [f for f in os.listdir(folder_path) if f.endswith(('.ogg'))]
        if sound_files:
            chosen_file = random.choice(sound_files)
            file_path = os.path.join(folder_path, chosen_file)
            self.media_player.setSource(qt2.QUrl.fromLocalFile(file_path))
            self.media_player.play()
    def open_user_g_window(self):
        webbrowser.open("https://drive.google.com/file/d/1GLp5kR6SIY2OhXfc6bZXjWn5beRflsEP/view?usp=drivesdk")
    def open_developers_window(self):
        self.developers_window = About_developers()
        self.developers_window.show()
    def viewInfoTextEdit(self):
        try:
            hijri_date_obj = Gregorian.today().to_hijri()
            if hijri_date_obj.month == 9:
                self.info.setText(_("رمضان كريم"))
            elif hijri_date_obj.month == 10 and hijri_date_obj.day == 1 or hijri_date_obj.month == 12 and hijri_date_obj.day == 10:
                self.info.setText(_("عيد مبارك"))
            elif hijri_date_obj.month == 10:
                self.info.setText(_("صيام الست أيام البيض في هذا الشهر وهي سنة عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month == 8:
                self.info.setText(_("يستحب الصيام في هذا الشهر"))
            elif hijri_date_obj.day in [13, 14, 15]:
                self.info.setText(_("صيام الأيام القمرية سنة عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month == 1 and hijri_date_obj.day == 10:
                self.info.setText(_("صيام عاشوراء مستحب عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month == 12 and hijri_date_obj.day in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.info.setText(_("صيام العشر الأوائل من ذي الحجة سنة عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month == 12 and hijri_date_obj.day == 9:
                self.info.setText(_("صيام وقفة عرفات"))
            elif datetime.datetime.now().weekday() in [0, 3]:
                self.info.setText(_("صيام اليوم سنة عن النبي صل الله عليه وسلم"))
            else:
                self.info.setText(_("لا تَنْسى ذِكْر الله"))
        except:
            self.info.setText(_("لا تَنْسى ذِكْر الله"))
    def onViewLastMessageButtonClicked(self):
        with open(os.path.join(os.getenv('appdata'), settings_handler.appName, "message.json"), "r", encoding="utf-8") as file:
            data = json.load(file)
        guiTools.TextViewer(self, _("آخر رسالة من المطورين"), data["message"]).exec()
    def whats_new_funktion(self):
        try:
            r = requests.get("https://raw.githubusercontent.com/mesteranas/{}/main/{}/update/app.json".format(settings_handler.appName, app.appdirname))
            info = r.json()
            guiTools.TextViewer(self, _("ما الجديد"), info["what is new"]).exec()
        except Exception as e:
            print(e)
            qt.QMessageBox.critical(self, _("خطأ"), _("فشلت عملية جلب المعلومات, الرجاء الإتصال بالإنترنت"))
    def license_funktion(self):
        try:
            r = requests.get("https://raw.githubusercontent.com/mesteranas/{}/main/LICENSE".format(settings_handler.appName))
            info = r.text
            guiTools.TextViewer(self, _("الترخيص"), info).exec()
        except Exception as e:
            print(e)
            qt.QMessageBox.critical(self, _("خطأ"), _("فشلت عملية جلب المعلومات, الرجاء الإتصال بالإنترنت"))
    def speac_info(self):
        guiTools.speak(_("للمزيد من الخيارات, الرجاء الضغت على زر alt"))
App = qt.QApplication([])
default_font = qt1.QFont()
default_font.setBold(True)
App.setFont(default_font)
App.setApplicationDisplayName(app.name)
App.setApplicationName(app.name)
App.setApplicationVersion(str(app.version))
App.setOrganizationName(app.creater)
App.setWindowIcon(qt1.QIcon("data/icons/app_icon.ico"))
App.setStyle('Fusion')
dark_palette = qt1.QPalette()
dark_palette.setColor(qt1.QPalette.ColorRole.Window, qt1.QColor("121212"))
dark_palette.setColor(qt1.QPalette.ColorRole.WindowText, qt1.QColor("#E0E0E0"))
dark_palette.setColor(qt1.QPalette.ColorRole.Base, qt1.QColor("#1E1E1E"))
dark_palette.setColor(qt1.QPalette.ColorRole.AlternateBase, qt1.QColor("#2C2C2C"))
dark_palette.setColor(qt1.QPalette.ColorRole.ToolTipBase, qt1.QColor("#2C2C2C"))
dark_palette.setColor(qt1.QPalette.ColorRole.ToolTipText, qt1.QColor("#E0E0E0"))
dark_palette.setColor(qt1.QPalette.ColorRole.Text, qt1.QColor("#E0E0E0"))
dark_palette.setColor(qt1.QPalette.ColorRole.Button, qt1.QColor("#2C2C2C"))
dark_palette.setColor(qt1.QPalette.ColorRole.ButtonText, qt1.QColor("#E0E0E0"))
dark_palette.setColor(qt1.QPalette.ColorRole.BrightText, qt1.QColor("#FF0000"))
dark_palette.setColor(qt1.QPalette.ColorRole.Highlight, qt1.QColor("#3A9FF5"))
dark_palette.setColor(qt1.QPalette.ColorRole.HighlightedText, qt1.QColor("#000000"))
App.setPalette(dark_palette)
window = main()
window.show()
App.exec()