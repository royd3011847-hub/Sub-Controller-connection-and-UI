from header import *


# ─────────────────────────────────────────────
#  BACKGROUND POLLING WORKER
# ─────────────────────────────────────────────
class TelemetryWorker(QThread):
    data_received  = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, get_url_fn, interval: float = 0.1):
        """
        get_url_fn : callable – returns the current base URL string.
                     Using a callable means URL changes (after CONNECT)
                     are picked up automatically without restarting the thread.
        interval   : polling period in seconds (default 100 ms).
        """
        super().__init__()
        self._get_url  = get_url_fn
        self._interval = interval
        self._running  = True

    def run(self):
        while self._running:
            try:
                url  = self._get_url() + "/odometry"
                resp = requests.get(url, timeout=1)
                if resp.ok:
                    self.data_received.emit(resp.json())
            except requests.exceptions.RequestException as e:
                self.error_occurred.emit(str(e))

            # Sleep in small ticks so stop() is responsive
            elapsed = 0.0
            tick    = 0.05
            while self._running and elapsed < self._interval:
                self.msleep(int(tick * 1000))
                elapsed += tick

    def stop(self):
        self._running = False
        self.wait()


# ─────────────────────────────────────────────
#  IMU TELEMETRY DISPLAY
# ─────────────────────────────────────────────
IMU_FIELDS = [
    ("POSITION",  [("X",      "x"),      ("Y",      "y"),      ("Z",      "z")]),
    ("VELOCITY",  [("VX",     "vx"),     ("VY",     "vy"),     ("VZ",     "vz")]),
    ("ACCEL",     [("AX",     "ax"),     ("AY",     "ay"),     ("AZ",     "az")]),
    ("ANGLE",     [("ROLL",   "roll"),   ("PITCH",  "pitch"),  ("YAW",    "yaw")]),
    ("ANG VEL",   [("VROLL",  "vroll"),  ("VPITCH", "vpitch"), ("VYAW",   "vyaw")]),
]

class TelemetryDisplay(QGroupBox):
    def __init__(self, parent=None, get_url=None):
        super().__init__("TELEMETRY", parent)
        self._labels: dict[str, QLabel] = {}
        self.get_url = get_url
        self._build_ui()
        self.running = True

        # Start the background polling thread only if a URL provider was given
        self._worker = None
        if callable(self.get_url):
            self._start_worker()

    # ── WORKER LIFECYCLE ─────────────────────
    def _start_worker(self):
        self._worker = TelemetryWorker(self.get_url)
        self._worker.data_received.connect(self.update_values)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    def set_url_provider(self, get_url_fn):
        """Call this after construction if get_url wasn't available at init time
        (e.g. when wiring up from SubmarineController after _build_ui)."""
        self.get_url = get_url_fn
        if self._worker is None:
            self._start_worker()

    def stop_worker(self):
        """Call from the parent window's closeEvent."""
        if self._worker and self._worker.isRunning():
            self._worker.stop()

    def _on_error(self, msg: str):
        # Silently swallow connection errors – the log panel in main handles them
        # if you want to surface them, emit a signal here instead.
        pass

    # ── UI BUILD ─────────────────────────────
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

    # ── DATA UPDATE (called by worker signal) ─
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
        

