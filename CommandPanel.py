from header import *


# ─────────────────────────────────────────────
#  AVAILABLE COMMANDS
#  Add new commands here — UI updates automatically
# ─────────────────────────────────────────────
COMMANDS = [
    "clear",
    "start telemetry",
    "stop telemetry",
]


class CommandPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("COMMANDS", parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(8, 8, 8, 8)

        for cmd in COMMANDS:
            row = QWidget()
            row.setStyleSheet(
                f"background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 3px;"
            )
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 4, 10, 4)

            lbl = QLabel(cmd)
            lbl.setFont(QFont("Courier New", 11))
            lbl.setStyleSheet(f"color: {COLORS['accent']}; border: none;")

            row_layout.addWidget(lbl)
            row_layout.addStretch()
            layout.addWidget(row)

        layout.addStretch()