import guiTools, requests, json, os, winsound, gui, functions
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
class DownloadThread(qt2.QThread):
    progress = qt2.pyqtSignal(int)
    finished = qt2.pyqtSignal()
    def __init__(self, url, filepath):
        super().__init__()
        self.url = url
        self.filepath = filepath
    def run(self):
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(self.filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    progress_percent = int((downloaded_size / total_size) * 100)
                    self.progress.emit(progress_percent)
            self.finished.emit()
class QuranPlayer(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("ctrl+s", self).activated.connect(lambda: self.mp.stop())
        qt1.QShortcut("space", self).activated.connect(self.play)
        qt1.QShortcut("alt+right", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 5000))
        qt1.QShortcut("alt+left", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 5000))
        qt1.QShortcut("alt+up", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 10000))
        qt1.QShortcut("alt+down", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 10000))
        qt1.QShortcut("ctrl+right", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 30000))
        qt1.QShortcut("ctrl+left", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 30000))
        qt1.QShortcut("ctrl+up", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 60000))
        qt1.QShortcut("ctrl+down", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 60000))
        qt1.QShortcut("ctrl+1", self).activated.connect(self.t10)
        qt1.QShortcut("ctrl+2", self).activated.connect(self.t20)
        qt1.QShortcut("ctrl+3", self).activated.connect(self.t30)
        qt1.QShortcut("ctrl+4", self).activated.connect(self.t40)
        qt1.QShortcut("ctrl+5", self).activated.connect(self.t50)
        qt1.QShortcut("ctrl+6", self).activated.connect(self.t60)
        qt1.QShortcut("ctrl+7", self).activated.connect(self.t70)
        qt1.QShortcut("ctrl+8", self).activated.connect(self.t80)
        qt1.QShortcut("ctrl+9", self).activated.connect(self.t90)
        qt1.QShortcut("shift+up", self).activated.connect(self.increase_volume)
        qt1.QShortcut("shift+down", self).activated.connect(self.decrease_volume)
        qt1.QShortcut("[", self).activated.connect(self.onChangeStartingPosition)
        qt1.QShortcut("]", self).activated.connect(self.onChangeEndingPosition)
        qt1.QShortcut("backspace", self).activated.connect(self.removePosition)
        self.bookmarksPosition = None
        self.isAMustToGoToBookmark = False
        self.startingPosition = None
        self.endingPosition = None
        self.repeatFromPositionToPosition = False
        self.reciters_data = self.load_reciters()
        self.recitersLabel = qt.QLabel(_("إختيار قارئ"))
        self.recitersLabel.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.reciterSearchLabel = qt.QLabel(_("ابحث عن قارئ"))
        self.reciterSearchLabel.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.reciterSearchEdit = qt.QLineEdit()
        self.reciterSearchEdit.setAccessibleName(_("ابحث عن قارئ"))
        self.reciterSearchEdit.setObjectName("reciterSearch")
        self.recitersListWidget = guiTools.QListWidget()
        self.recitersListWidget.itemSelectionChanged.connect(self.on_reciter_selected)
        self.surahsLabel = qt.QLabel(_("السور"))
        self.surahsLabel.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.surahSearchLabel = qt.QLabel(_("ابحث عن سورة"))
        self.surahSearchLabel.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.surahSearchEdit = qt.QLineEdit()
        self.surahSearchEdit.setAccessibleName(_("ابحث عن سورة"))
        self.surahSearchEdit.setObjectName("surahSearch")
        self.surahListWidget = guiTools.QListWidget()
        self.surahListWidget.clicked.connect(self.play_selected_audio)
        self.reciterSearchEdit.textChanged.connect(self.reciter_onsearch)
        self.surahSearchEdit.textChanged.connect(self.surah_onsearch)
        self.recitersList = list(self.reciters_data.keys())
        self.recitersList.sort()
        self.recitersListWidget.addItems(self.recitersList)
        self.progressBar = qt.QProgressBar()
        self.progressBar.setFocusPolicy(qt2.Qt.FocusPolicy.StrongFocus)
        self.progressBar.setVisible(False)
        self.mp = QMediaPlayer()
        self.au = QAudioOutput()
        self.mp.setAudioOutput(self.au)
        self.openBookmarks = qt.QPushButton(_("العلامات المرجعية"))
        self.openBookmarks.setDefault(True)
        self.openBookmarks.clicked.connect(self.onBookmarkOpened)
        self.openBookmarks.setShortcut("ctrl+shift+b")
        self.openBookmarks.setAccessibleDescription("control plus shift plus b")
        self.openBookmarks.setFixedSize(150, 40)
        self.play_all_to_end = qt.QPushButton(_("تشغيل كل السور من بداية السورة المركز عليها الى النهاية"))
        self.play_all_to_end.setAccessibleDescription("control plus A")
        self.play_all_to_end.setCheckable(True)
        self.play_all_to_end.setDefault(True)
        self.play_all_to_end.setShortcut("ctrl+a")
        self.play_all_to_end.toggled.connect(lambda checked: self.update_button_style(self.play_all_to_end, checked))
        self.play_all_to_end.toggled.connect(self.handle_play_all_toggled)
        self.play_all_to_start = qt.QPushButton(_("تشغيل كل السور من بداية السورة المركز عليها الى البداية"))
        self.play_all_to_start.setAccessibleDescription("control plus shift plus A")
        self.play_all_to_start.setCheckable(True)
        self.play_all_to_start.setDefault(True)
        self.play_all_to_start.setShortcut("ctrl+shift+a")
        self.play_all_to_start.toggled.connect(lambda checked: self.update_button_style(self.play_all_to_start, checked))
        self.play_all_to_start.toggled.connect(self.handle_play_all_start_toggled)
        self.repeat_surah_button = qt.QPushButton(_("تكرار تشغيل السورة المحددة"))
        self.repeat_surah_button.setAccessibleDescription("control plus R")
        self.repeat_surah_button.setCheckable(True)
        self.repeat_surah_button.setDefault(True)
        self.repeat_surah_button.setShortcut("ctrl+r")
        self.repeat_surah_button.toggled.connect(lambda checked: self.update_button_style(self.repeat_surah_button, checked))
        self.repeat_surah_button.toggled.connect(self.handle_repeat_toggled)
        self.Slider = qt.QSlider(qt2.Qt.Orientation.Horizontal)
        self.Slider.setRange(0, 100)
        self.Slider.setAccessibleName(_("الوقت المنقدي"))
        self.Slider.setTracking(True)
        self.Slider.valueChanged.connect(self.set_position_from_slider)
        self.Slider.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.Slider.customContextMenuRequested.connect(self.onAddNewBookmark)
        self.mp.durationChanged.connect(self.update_slider)
        self.mp.positionChanged.connect(self.update_slider)
        self.duration = qt.QLineEdit()
        self.duration.setReadOnly(True)
        self.duration.setAccessibleName(_("مدة المقطع"))
        self.duration.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.mp.mediaStatusChanged.connect(self.handle_media_status_changed)
        self.dl_all_app = qt.QPushButton(_("تحميل جميع السور المتاحة لهذا القارئ في التطبيق"))
        self.dl_all_app.setDefault(True)
        self.dl_all_app.clicked.connect(self.download_all_audios_to_app)
        self.dl_all = qt.QPushButton(_("تحميل جميع السور المتاحة لهذا القارئ في الجهاز"))
        self.dl_all.setDefault(True)
        self.dl_all.clicked.connect(self.download_all_soar)
        self.delete = qt.QPushButton(_("حذف كل السور للقارئ الحالي من التطبيق"))
        self.delete.setStyleSheet("background-color: #8B0000; color: white;")
        self.delete.setDefault(True)
        self.delete.setVisible(False)
        self.delete.clicked.connect(lambda: self.delete_surah())
        self.user_guide = qt.QPushButton(_("دليل الاختصارات"))
        self.user_guide.setDefault(True)
        self.user_guide.setShortcut("ctrl+f1")
        self.user_guide.setAccessibleDescription(_("control plus f1"))
        self.user_guide.setFixedSize(150, 40)
        self.user_guide.clicked.connect(lambda: guiTools.TextViewer(
            self,
            _("دليل الاختصارات"),
            _("ctrl+s: إيقاف\nspace: التشغيل والإيقاف المؤقت\nalt زائد السهم الأيمن: التقديم السريع لمدة 5 ثواني\n"
              "alt زائد السهم الأيسر: الترجيع السريع لمدة 5 ثواني\nalt زائد السهم الأعلى: التقديم السريع لمدة 10 ثواني\n"
              "alt زائد السهم الأسفل: الترجيع السريع لمدة 10 ثواني\nctrl زائد السهم الأيمن: التقديم السريع لمدة 30 ثانية\n"
              "ctrl زائد السهم الأيسر: الترجيع السريع لمدة 30 ثانية\nctrl زائد السهم الأعلى: التقديم السريع لمدة دقيقة\n"
              "ctrl زائد السهم الأسفل: الترجيع  السريع لمدة دقيقة\nctrl زائد رقم: الانتقال الى موضع محدد من المقطع, مثلا ctrl+10 الانتقال الى 10% من المقطع\n"
              "shift زائد السهم الأعلى: رفع الصوت\nshift زائد السهم الأسفل: خفض الصوت\n[: تحديد موضع البدء\n"
              "]: تحديد موضع الانتهاء\nbackspace: حذف الموضع المحدد وإيقاف التكرار\n"
              "الضغط على زر التطبيقات على شريط مدة المقطع يسمح بإضافة علامة مرجعية للموضع الحالي\n"
              "ctrl+shift+b: فتح نافذة العلامات المرجعية\nctrl+f1: دليل الاختصارات")
        ).exec())
        recitersLayout = qt.QVBoxLayout()
        recitersLayout.addWidget(self.recitersLabel)
        recitersLayout.addWidget(self.reciterSearchLabel)
        recitersLayout.addWidget(self.reciterSearchEdit)
        recitersLayout.addWidget(self.recitersListWidget)
        surahsLayout = qt.QVBoxLayout()
        surahsLayout.addWidget(self.surahsLabel)
        surahsLayout.addWidget(self.surahSearchLabel)
        surahsLayout.addWidget(self.surahSearchEdit)
        surahsLayout.addWidget(self.surahListWidget)
        topLayout = qt.QHBoxLayout()
        topLayout.addLayout(recitersLayout)
        topLayout.addLayout(surahsLayout)
        layout = qt.QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.dl_all_app)
        layout.addWidget(self.delete)
        layout.addWidget(self.dl_all)
        layout.addWidget(self.Slider)
        layout.addWidget(self.play_all_to_end)
        layout.addWidget(self.play_all_to_start)
        layout.addWidget(self.repeat_surah_button)
        layout.addWidget(self.progressBar)
        layout1 = qt.QHBoxLayout()
        layout1.addWidget(self.user_guide)
        layout1.addWidget(self.duration)
        layout1.addWidget(self.openBookmarks)
        layout.addLayout(layout1)
        self.setLayout(layout)
        if self.recitersListWidget.count() > 0:
            self.recitersListWidget.setCurrentRow(0)
            self.on_reciter_selected()
        self.surahListWidget.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.surahListWidget.customContextMenuRequested.connect(self.open_context_menu)
    def update_button_style(self, button, checked):
        if checked:
            button.setStyleSheet("background-color: blue; color: white;")
        else:
            button.setStyleSheet("")
    def handle_play_all_toggled(self, checked):
        self.mp.stop()
        if checked:
            self.play_all_to_start.setEnabled(False)
            self.repeat_surah_button.setEnabled(False)
            if self.surahListWidget.currentRow() == -1 and self.surahListWidget.count() > 0:
                self.surahListWidget.setCurrentRow(0)
            self.play_selected_audio()
        else:
            self.play_all_to_start.setEnabled(True)
            self.repeat_surah_button.setEnabled(True)
    def handle_play_all_start_toggled(self, checked):
        self.mp.stop()
        if checked:
            self.play_all_to_end.setEnabled(False)
            self.repeat_surah_button.setEnabled(False)
            if self.surahListWidget.currentRow() == -1 and self.surahListWidget.count() > 0:
                self.surahListWidget.setCurrentRow(self.surahListWidget.count() - 1)
            self.play_selected_audio()
        else:
            self.play_all_to_end.setEnabled(True)
            self.repeat_surah_button.setEnabled(True)
    def handle_repeat_toggled(self, checked):
        self.mp.stop()
        if checked:
            self.play_all_to_end.setEnabled(False)
            self.play_all_to_start.setEnabled(False)
        else:
            self.play_all_to_end.setEnabled(True)
            self.play_all_to_start.setEnabled(True)
    def handle_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.repeat_surah_button.isChecked():
                self.mp.setPosition(0)
                self.play_selected_audio()
            elif self.play_all_to_end.isChecked():
                self.play_next_in_list()
            elif self.play_all_to_start.isChecked():
                self.play_previous_in_list()
    def play_next_in_list(self):
        current_row = self.surahListWidget.currentRow()
        if current_row < self.surahListWidget.count() - 1:
            self.surahListWidget.setCurrentRow(current_row + 1)
            self.play_selected_audio()
        else:
            self.play_all_to_end.setChecked(False)
    def play_previous_in_list(self):
        current_row = self.surahListWidget.currentRow()
        if current_row > 0:
            self.surahListWidget.setCurrentRow(current_row - 1)
            self.play_selected_audio()
        else:
            self.play_all_to_start.setChecked(False)
    def delete_surah(self, surah_name=None):
        selected_reciter_item = self.recitersListWidget.currentItem()
        if not selected_reciter_item:
            return
        reciter = selected_reciter_item.text()
        reciter_folder = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter)
        try:
            if surah_name:
                surah_path = os.path.join(reciter_folder, f"{surah_name}.mp3")
                if os.path.exists(surah_path):
                    confirm = qt.QMessageBox.question(
                        self,
                        _("تأكيد الحذف"),
                        _("هل أنت متأكد أنك تريد حذف السورة المحددة؟"),
                        qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No,
                        qt.QMessageBox.StandardButton.No,
                    )
                    if confirm == qt.QMessageBox.StandardButton.Yes:
                        try:
                            os.remove(surah_path)
                            qt.QMessageBox.information(self, _("تم"), _("تم حذف السورة بنجاح."))
                        except PermissionError:
                            qt.QMessageBox.critical(self, _("خطأ"), _("تعذر حذف السورة. قد تكون قيد الاستخدام, يرجى إعادة تشغيل البرنامج"))
            else:
                if os.path.exists(reciter_folder):
                    confirm = qt.QMessageBox.question(
                        self,
                        _("تأكيد الحذف"),
                        _("هل أنت متأكد أنك تريد حذف جميع السور؟"),
                        qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No,
                        qt.QMessageBox.StandardButton.No,
                    )
                    if confirm == qt.QMessageBox.StandardButton.Yes:
                        for file in os.listdir(reciter_folder):
                            if file.endswith(".mp3"):
                                try:
                                    os.remove(os.path.join(reciter_folder, file))
                                except PermissionError:
                                    qt.QMessageBox.critical(
                                        self,
                                        _("خطأ"),
                                        _("تعذر حذف بعض الملفات. قد تكون قيد الاستخدام, يرجى إعادة تشغيل البرنامج")
                                    )
                        qt.QMessageBox.information(self, _("تم"), _("تم حذف جميع السور بنجاح."))
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ غير متوقع"), str(e))
        self.check_all_surahs_downloaded()
    def check_all_surahs_downloaded(self):
        selected_reciter_item = self.recitersListWidget.currentItem()
        if selected_reciter_item:
            reciter = selected_reciter_item.text()
            reciter_folder = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter)
            if os.path.exists(reciter_folder):
                all_files = os.listdir(reciter_folder)
                all_surahs = self.reciters_data.get(reciter, {}).keys()
                downloaded_surahs = {os.path.splitext(file)[0] for file in all_files if file.endswith(".mp3")}
                if downloaded_surahs >= set(all_surahs):
                    self.delete.setVisible(True)
                    self.dl_all_app.setVisible(False)
                else:
                    self.delete.setVisible(False)
                    self.dl_all_app.setVisible(True)
            else:
                self.delete.setVisible(False)
                self.dl_all_app.setVisible(True)
    def check_current_surah_downloaded(self):        
        selected_reciter_item = self.recitersListWidget.currentItem()
        if not selected_reciter_item:
            return
        reciter = selected_reciter_item.text()
        selected_item = self.surahListWidget.currentItem()
        if not selected_item:
            return
        surah_name = selected_item.text()
        surah_path = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter, f"{surah_name}.mp3")
        if os.path.exists(surah_path):
            action = qt.QWidgetAction(self)
            btn = qt.QPushButton(_("حذف السورة المحددة من التطبيق"))
            btn.setStyleSheet("background-color: #8B0000; color: white;")
            btn.setDefault(True)
            btn.clicked.connect(lambda: self.delete_surah(surah_name))
            action.setDefaultWidget(btn)
            return action
        return None
    def download_selected_audio_to_app(self):
        try:
            selected_reciter_item = self.recitersListWidget.currentItem()
            if not selected_reciter_item:
                return
            reciter = selected_reciter_item.text()
            selected_item = self.surahListWidget.currentItem()
            if selected_item:
                url = self.reciters_data[reciter][selected_item.text()]
                audio_folder = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter)
                os.makedirs(audio_folder, exist_ok=True)
                filepath = os.path.join(audio_folder, f"{selected_item.text()}.mp3")
                if self.is_audio_downloaded(filepath):
                    qt.QMessageBox.critical(self, _("تنبيه"), _("السورة محملة بالفعل."))
                    return
                self.progressBar.setVisible(True)
                self.download_thread = DownloadThread(url, filepath)
                self.download_thread.progress.connect(self.progressBar.setValue)
                self.download_thread.finished.connect(self.download_audio_complete)
                self.download_thread.start()
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"), _("حدث خطأ أثناء تحميل المقطع: ") + str(e))
    def download_all_audios_to_app(self):
        try:
            selected_reciter_item = self.recitersListWidget.currentItem()
            if not selected_reciter_item:
                return
            reciter = selected_reciter_item.text()
            self.files_to_download = [
                (file_name, url)
                for file_name, url in self.reciters_data.get(reciter, {}).items()
                if not self.is_audio_downloaded(
                    os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter, f"{file_name}.mp3")
                )
            ]
            self.current_file_index = 0
            if not self.files_to_download:
                qt.QMessageBox.critical(self, _("تنبيه"), _("جميع السور محملة بالفعل"))
                return
            response = qt.QMessageBox.question(
                self,
                _("تأكيد التحميل"),
                _("هل تريد تحميل جميع السور المتاحة لهذا القارئ؟"),
                qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No,
                qt.QMessageBox.StandardButton.No,
            )
            if response == qt.QMessageBox.StandardButton.Yes:
                app_folder = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter)
                os.makedirs(app_folder, exist_ok=True)
                self.save_folder = app_folder
                self.download_next_audio_to_app()
            else:
                qt.QMessageBox.information(self, _("إلغاء العملية"), _("تم إلغاء تحميل السور."))
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"), _("حدث خطأ أثناء بدء التحميل: ") + str(e))
    def is_audio_downloaded(self, filepath):
        return os.path.exists(filepath)
    def download_next_audio_to_app(self):
        if self.current_file_index < len(self.files_to_download):
            file_name, url = self.files_to_download[self.current_file_index]
            filepath = os.path.join(self.save_folder, f"{file_name}.mp3")
            self.current_file_index += 1
            self.progressBar.setVisible(True)
            self.download_thread = DownloadThread(url, filepath)
            self.download_thread.progress.connect(self.progressBar.setValue)
            self.download_thread.finished.connect(self.download_next_audio_to_app)
            self.download_thread.start()
        else:
            self.progressBar.setVisible(False)
            qt.QMessageBox.information(self, _("تم"), _("تم تحميل جميع السور بنجاح."))
    def download_audio_complete(self):
        self.progressBar.setValue(100)
        self.progressBar.setVisible(False)
        qt.QMessageBox.information(self, _("تم"), _("تم تحميل السورة بنجاح."))
    def download_all_soar(self):
        selected_reciter_item = self.recitersListWidget.currentItem()
        if not selected_reciter_item:
            return
        reciter_name = selected_reciter_item.text()
        self.files_to_download = list(self.reciters_data.get(reciter_name, {}).items())
        self.current_file_index = 0
        save_folder = qt.QFileDialog.getExistingDirectory(self, _("اختيار مجلد لحفظ السور"))
        if not save_folder:
            return
        response = qt.QMessageBox.question(self, _("تأكيد التحميل"),
            _("هل أنت متأكد من تحميل جميع السور؟"),
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No,
            qt.QMessageBox.StandardButton.No)
        if response == qt.QMessageBox.StandardButton.Yes:
            self.save_folder = save_folder
            self.download_next_sora()
        else:
            qt.QMessageBox.information(self, _("إلغاء التحميل"), _("تم إلغاء التحميل."))
    def download_next_sora(self):
        if self.current_file_index < len(self.files_to_download):
            file_name, url = self.files_to_download[self.current_file_index]
            filepath = f"{self.save_folder}/{file_name}.mp3"
            self.current_file_index += 1
            self.download_thread = DownloadThread(url, filepath)
            self.download_thread.progress.connect(self.update_progress)
            self.download_thread.finished.connect(self.download_finished)
            self.download_thread.start()
        else:
            self.progressBar.setVisible(False)
            qt.QMessageBox.information(self, _("تم التحميل"), _("تم تحميل جميع السور."))
    def update_progress(self, progress_percent):
        self.progressBar.setValue(progress_percent)
    def download_finished(self):
        self.progressBar.setVisible(True)
        self.download_next_sora()
    def download_complete(self):
        self.progressBar.setVisible(False)
        qt.QMessageBox.information(self, _("تم"), _("تم تحميل السورة"))
    def on_reciter_selected(self):
        self.mp.stop()
        self.surahListWidget.clear()
        selected_reciter_item = self.recitersListWidget.currentItem()
        if selected_reciter_item:
            reciter = selected_reciter_item.text()
            for surah, link in self.reciters_data[reciter].items():
                self.surahListWidget.addItem(surah)
            self.check_all_surahs_downloaded()
    def search(self, search_text, data):
        return [item for item in data if search_text in item.lower()]
    def reciter_onsearch(self):
        search_text = self.reciterSearchEdit.text().lower()
        self.recitersListWidget.clear()
        result = self.search(search_text, self.recitersList)
        self.recitersListWidget.addItems(result)
    def surah_onsearch(self):
        search_text = self.surahSearchEdit.text().lower()
        self.surahListWidget.clear()
        selected_reciter_item = self.recitersListWidget.currentItem()
        if selected_reciter_item:
            reciter = selected_reciter_item.text()
            surah_list = list(self.reciters_data[reciter].keys())
        else:
            surah_list = []
        result = self.search(search_text, surah_list)
        self.surahListWidget.addItems(result)
    def play_selected_audio(self):
        self.repeatFromPositionToPosition = False
        try:
            selected_reciter_item = self.recitersListWidget.currentItem()
            if not selected_reciter_item:
                return
            reciter = selected_reciter_item.text()
            selected_item = self.surahListWidget.currentItem()
            if selected_item:
                audio_folder = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter)
                audio_path = os.path.join(audio_folder, selected_item.text() + ".mp3")
                if os.path.exists(audio_path):
                    self.mp.setSource(qt2.QUrl.fromLocalFile(audio_path))
                    self.mp.play()
                else:
                    url = self.reciters_data[reciter][selected_item.text()]
                    self.mp.setSource(qt2.QUrl(url))
                    self.mp.play()
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"), _("حدث خطأ أثناء تشغيل المقطع:") + str(e))
    def download_selected_audio(self):
        try:
            selected_reciter_item = self.recitersListWidget.currentItem()
            if not selected_reciter_item:
                return
            reciter = selected_reciter_item.text()
            selected_item = self.surahListWidget.currentItem()
            if selected_item:
                url = self.reciters_data[reciter][selected_item.text()]
                filepath, _ = qt.QFileDialog.getSaveFileName(self, "save surah", "", "Audio Files (*.mp3)")
                if filepath:
                    self.progressBar.setVisible(True)
                    self.download_thread = DownloadThread(url, filepath)
                    self.download_thread.progress.connect(self.progressBar.setValue)
                    self.download_thread.finished.connect(self.download_complete)
                    self.download_thread.start()
        except:
            qt.QMessageBox.critical(self, _("تنبيه"), _("حدث خطأ ما"))
    def open_context_menu(self, position):
        menu = qt.QMenu(self)
        repeateFromPositionTopositionMenue = menu.addMenu(_("التكرار من موضع إلى موضع"))
        setStartingPositionAction = qt1.QAction(_("تحديد موضع البداية"), self)
        setStartingPositionAction.triggered.connect(self.onChangeStartingPosition)
        repeateFromPositionTopositionMenue.addAction(setStartingPositionAction)
        repeateFromPositionTopositionMenue.setDefaultAction(setStartingPositionAction)
        setEndingPositionAction = qt1.QAction(_("تحديد موضع النهاية"), self)
        setEndingPositionAction.triggered.connect(self.onChangeEndingPosition)
        repeateFromPositionTopositionMenue.addAction(setEndingPositionAction)
        resetAndStopRepeatingAction = qt1.QAction("حذف الموضع المحدد وإيقاف التكرار", self)
        resetAndStopRepeatingAction.triggered.connect(self.removePosition)
        repeateFromPositionTopositionMenue.addAction(resetAndStopRepeatingAction)
        play_action = qt1.QAction(_("تشغيل السورة المحددة"), self)
        play_action.triggered.connect(self.play_selected_audio)
        menu.addAction(play_action)
        selected_item = self.surahListWidget.currentItem()
        if selected_item:
            surah_name = selected_item.text()
            selected_reciter_item = self.recitersListWidget.currentItem()
            if not selected_reciter_item:
                return
            reciter = selected_reciter_item.text()
            surah_path = os.path.join(os.getenv('appdata'), app.appName, "quran surah reciters", reciter, f"{surah_name}.mp3")
            if not os.path.exists(surah_path):
                download_app_action = qt1.QAction(_("تحميل السورة المحددة في التطبيق"), self)
                download_app_action.triggered.connect(self.download_selected_audio_to_app)
                menu.addAction(download_app_action)
            download_device_action = qt1.QAction(_("تحميل السورة المحددة في الجهاز"), self)
            download_device_action.triggered.connect(self.download_selected_audio)
            menu.addAction(download_device_action)
        delete_option = self.check_current_surah_downloaded()
        if delete_option:
            menu.addAction(delete_option)
        addNewBookmarkAction = qt1.QAction(_("إضافة علامة مرجعية"), self)
        menu.addAction(addNewBookmarkAction)
        addNewBookmarkAction.triggered.connect(self.onAddNewBookmark)
        menu.exec(self.surahListWidget.viewport().mapToGlobal(position))
    def t10(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.1))
    def t20(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.2))
    def t30(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.3))
    def t40(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.4))
    def t50(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.5))
    def t60(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.6))
    def t70(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.7))
    def t80(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.8))
    def t90(self):
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.9))
    def play(self):
        if self.mp.isPlaying():
            self.mp.pause()
        else:
            self.mp.play()
    def increase_volume(self):
        current_volume = self.au.volume()
        new_volume = current_volume + 0.10
        self.au.setVolume(new_volume)
    def decrease_volume(self):
        current_volume = self.au.volume()
        new_volume = current_volume - 0.10
        self.au.setVolume(new_volume)
    def set_position_from_slider(self, value):
        duration = self.mp.duration()
        new_position = int((value / 100) * duration)
        self.mp.setPosition(new_position)
    def update_slider(self):
        if self.isAMustToGoToBookmark and self.mp.position() >= 3000:
            self.isAMustToGoToBookmark = False
            self.mp.setPosition(self.bookmarksPosition)
        if self.repeatFromPositionToPosition:
            if self.mp.position() >= self.endingPosition:
                self.mp.pause()
                self.mp.setPosition(self.startingPosition)
                self.mp.play()
                return
        try:
            self.Slider.blockSignals(True)
            self.Slider.setValue(int((self.mp.position() / self.mp.duration()) * 100))
            self.Slider.blockSignals(False)
            self.time_VA()
        except:
            self.duration.setText(_("خطأ في الحصول على مدة المقطع"))
    def time_VA(self):
        position = self.mp.position()
        duration = self.mp.duration()
        remaining = duration - position
        position_str = qt2.QTime(0, 0, 0).addMSecs(position).toString("HH:mm:ss")
        duration_str = qt2.QTime(0, 0, 0).addMSecs(duration).toString("HH:mm:ss")
        remaining_str = qt2.QTime(0, 0, 0).addMSecs(remaining).toString("HH:mm:ss")
        self.duration.setText(
            _("الوقت المنقضي: ") + position_str +
            _("، الوقت المتبقي: ") + remaining_str +
            _("، مدة المقطع: ") + duration_str
        )
    @staticmethod
    def load_reciters():
        file_path = "data/json/reciters.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    def onChangeStartingPosition(self):
        position = self.mp.position()
        self.startingPosition = position
        self.endingPosition = None
        self.repeatFromPositionToPosition = False
        winsound.Beep(400, 500)
    def onChangeEndingPosition(self):
        if self.startingPosition is not None:
            if self.startingPosition == self.mp.position():
                qt.QMessageBox.critical(self, _("خطأ"), _("لا يمكن أن يكون موضع البداية هو نفس موضع النهاية"))
            elif self.startingPosition > self.mp.position():
                qt.QMessageBox.critical(self, _("خطأ"), _("لا يمكن أن يكون موضع البداية أكبر من موضع النهاية"))
            else:
                position = self.mp.position()
                self.endingPosition = position
                winsound.Beep(500, 500)
                self.repeatFromPositionToPosition = True
                self.mp.setPosition(self.startingPosition)
        else:
            qt.QMessageBox.critical(self, _("خطأ"), _("يرجى تحديد موضع البداية أولا"))
    def removePosition(self):
        self.startingPosition = None
        self.endingPosition = None
        self.repeatFromPositionToPosition = False
        winsound.Beep(300, 500)
    def onBookmarkOpened(self):
        gui.book_marcks(self, "quran").exec()
    def onAddNewBookmark(self):
        name, ok = guiTools.QInputDialog.getText(self, _("إضافة علامة مرجعية"), _("أكتب اسم العلامة المرجعية"))
        if ok:
            type = self.recitersListWidget.currentRow()
            surah = self.surahListWidget.currentRow()
            position = self.mp.position()
            functions.bookMarksManager.addNewaudioBookMark("quran", type, surah, position, name)
    def onRemoveBookmark(self):
        try:
            functions.bookMarksManager.removeaudioBookMark("quran",self.nameOfBookmark)
            qt.QMessageBox.information(self,_("تم"),_("تم الحذف"))
        except:
            qt.QMessageBox.critical(self,_("خطأ"),_("تعذر حذف العلامة المرجعية"))