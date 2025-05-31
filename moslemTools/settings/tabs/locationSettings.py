from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import os, shutil,guiTools
class LocationSettings(qt.QWidget):
    def __init__(self, p):
        super().__init__()
        self.setStyleSheet("""            
            }
            QCheckBox, QLineEdit {                
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 4px;
            }
            QPushButton {
                background-color: #0000AA; /* اللون الأزرق من شاشة الموت */
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 6px;
            }
        """)
        layout = qt.QVBoxLayout(self)
        self.autoDetectLocation=qt.QCheckBox(_("تحديد الموقع تلقائي"))
        self.autoDetectLocation.setChecked(p.cbts(settings_handler.get("location","autoDetect")))
        self.autoDetectLocation.stateChanged.connect(self.onStateChanged)
        layout.addWidget(self.autoDetectLocation)
        self.LT1=qt.QDoubleSpinBox()
        self.LT1.setAccessibleName(_("خط الطول"))
        self.LT1.setRange(0.0001,360.0000)
        self.LT1.setDecimals(4)
        self.LT1.setValue(float(settings_handler.get("location","LT1")))
        self.LT1.setVisible(p.cbts(settings_handler.get("location","autoDetect"))==False)
        layout.addWidget(self.LT1)
        self.LT2=qt.QDoubleSpinBox()
        self.LT2.setAccessibleName(_("دائرة العرض"))
        self.LT2.setRange(0,180)
        self.LT2.setValue(float(settings_handler.get("location","LT2")))
        self.LT2.setDecimals(4)
        self.LT2.setVisible(p.cbts(settings_handler.get("location","autoDetect"))==False)
        layout.addWidget(self.LT2)
    def onStateChanged(self,state):
        self.LT1.setVisible(state==False)
        self.LT2.setVisible(state==False)