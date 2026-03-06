
from main import *
from header import *

class LogPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("COMM LOG", parent)
        layout = QVBoxLayout(self)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumHeight(130)
        layout.addWidget(self._log)

    def append(self, message: str, level: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        colors = {
            "ok":   COLORS["accent"],
            "err":  COLORS["danger"],
            "warn": COLORS["warn"],
            "send": COLORS["mode_imu"],
            "info": COLORS["text_secondary"],
        }
        c = colors.get(level, COLORS["text_secondary"])
        self._log.append(
            f'<span style="color:{COLORS["text_dim"]}">[{ts}]</span> '
            f'<span style="color:{c}">{message}</span>'
        )
        self._log.verticalScrollBar().setValue(
            self._log.verticalScrollBar().maximum()
        )
    def clear(self):
        self._log.clear()