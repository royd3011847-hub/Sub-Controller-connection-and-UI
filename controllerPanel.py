from concurrent.futures import process

from header import *
from Theme import *


class ControllerPanel(QWidget):
    command_ready = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        desc = QLabel(
            "CONTROLLER MODE\n\n"
            "Use an attached game controller lil bro\n"\
        )
        desc.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 11px; "
            f"letter-spacing: 1px; border: 1px solid {COLORS['border']}; "
            f"background: {COLORS['bg_card']}; padding: 1px; border-radius: 4px;"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # add a terminal with QProcess
        # allow user to send commands
        process = QProcess()
        process.start("python3", ["controller_terminal.py"])
        
        