from header import *


# ─────────────────────────────────────────────
#  IMU TELEMETRY DISPLAY
# ─────────────────────────────────────────────
IMU_FIELDS = [
    ("POSITION",  [("X",  "x"),  ("Y",  "y"),  ("Z",  "z")]),
    ("VELOCITY",  [("VX", "vx"), ("VY", "vy"), ("VZ", "vz")]),
    ("ACCEL",     [("AX", "ax"), ("AY", "ay"), ("AZ", "az")]),
    ("ANGLE",  [("ROLL", "roll"), ("PITCH", "pitch"), ("YAW", "yaw")]),
    ("ANG VEL",   [("VROLL", "vroll"), ("VPITCH", "vpitch"), ("VYAW", "vyaw")]),
]

class TelemetryDisplay(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("TELEMETRY", parent)
        self._labels: dict[str, QLabel] = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(2)

        for group_name, fields in IMU_FIELDS:
            row_widget = QWidget()
            row_widget.setStyleSheet(
                f"background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 3px;"
            )
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(0)

            # group label
            grp_lbl = QLabel(group_name)
            grp_lbl.setFont(QFont("Courier New", 13))
            grp_lbl.setStyleSheet(f"color: {COLORS['text_dim']}; letter-spacing: 1px; border: none;")
            grp_lbl.setFixedWidth(100)
            row_layout.addWidget(grp_lbl)

            # separator
            sep = QFrame()
            sep.setFrameShape(QFrame.Shape.VLine)
            sep.setStyleSheet(f"background: {COLORS['border']}; border: none; max-width: 1px;")
            sep.setFixedWidth(1)
            row_layout.addWidget(sep)
            row_layout.addSpacing(15)

            for label_text, key in fields:
                cell = QWidget()
                cell_layout = QVBoxLayout(cell)
                cell_layout.setContentsMargins(4, 2, 4, 2)
                cell_layout.setSpacing(1)

                name_lbl = QLabel(label_text)
                name_lbl.setFont(QFont("Courier New", 12))
                name_lbl.setStyleSheet(f"color: {COLORS['text_dim']}; border: none;")
                name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

                val_lbl = QLabel("——")
                val_lbl.setFont(QFont("Courier New", 15))
                val_lbl.setStyleSheet(f"color: {COLORS['accent']}; border: none;")
                val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                val_lbl.setMinimumWidth(120)

                cell_layout.addWidget(name_lbl)
                cell_layout.addWidget(val_lbl)
                row_layout.addWidget(cell)

                self._labels[key] = val_lbl

            row_layout.addStretch()
            layout.addWidget(row_widget)

    def update_values(self, data: dict):
        for key, lbl in self._labels.items():
            if key in data:
                val = data[key]
                lbl.setText(f"{val:+.3f}" if isinstance(val, float) else str(val))
                lbl.setStyleSheet(f"color: {COLORS['accent']}; border: none;")
            else:
                lbl.setText("——")
                lbl.setStyleSheet(f"color: {COLORS['text_dim']}; border: none;")
        #format:
        # if value is a float, show with 3 decimal places and a + sign for positive numbers
        # if value is missing, show "——" and dim the color
        #dict input example:
        # {
        #     "x": 1.23,
        #     "y": 4.56,
        #     "z": 7.89,
        #     "vx": 0.12,
        #     "vy": 0.34,
        #     "vz": 0.56,
        #     "ax": 0.01,
        #     "ay": 0.02,
        #     "az": 0.03,
        #     "roll": 10.0,
        #     "pitch": 20.0,
        #     "yaw": 30.0,
        #     "vroll": 0.1,
        #     "vpitch": 0.2,
        #     "vyaw": 0.3,
        # }
        

