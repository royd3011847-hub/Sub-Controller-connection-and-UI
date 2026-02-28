from main import *
from header import *

class ScriptPanel(QWidget):
    command_ready = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        desc = QLabel(
            "AUTONOMOUS SCRIPT MODE\n\n"
            "The submarine will execute its onboard autonomous program.\n"
            "Manual IMU overrides are disabled while a script is running."
        )
        desc.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 11px; "
            f"letter-spacing: 1px; border: 1px solid {COLORS['border']}; "
            f"background: {COLORS['bg_card']}; padding: 16px; border-radius: 4px;"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # big run button
        self._btn_run = QPushButton("◉  EXECUTE AUTONOMOUS SCRIPT")
        self._btn_run.setObjectName("btn_script")
        self._btn_run.setMinimumHeight(60)
        self._btn_run.clicked.connect(self._toggle_script)
        layout.addWidget(self._btn_run)

        # stop button
        self._btn_stop = QPushButton("■  ABORT SCRIPT")
        self._btn_stop.setEnabled(False)
        self._btn_stop.setStyleSheet(
            f"background: #200a0a; border: 1px solid {COLORS['danger']}; "
            f"color: {COLORS['danger']}; font-size: 12px; letter-spacing: 3px; padding: 10px;"
        )
        self._btn_stop.clicked.connect(self._stop_script)
        layout.addWidget(self._btn_stop)

        layout.addStretch()

    def _toggle_script(self):
        self._running = True
        self._btn_run.setEnabled(False)
        self._btn_stop.setEnabled(True)
        self._btn_run.setText("◉  SCRIPT RUNNING...")
        self.command_ready.emit({"mode": "script", "action": "start"})

    def _stop_script(self):
        self._running = False
        self._btn_run.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._btn_run.setText("◉  EXECUTE AUTONOMOUS SCRIPT")
        self.command_ready.emit({"mode": "script", "action": "stop"})

    def reset(self):
        self._stop_script()
