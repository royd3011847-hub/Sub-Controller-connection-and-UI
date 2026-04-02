from header import *

class BoxesWorker(QThread):
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
        print("boxes run")
        # this is the IMUDisplay run code
        # When we get a url and an API call for this, that is what we will use
        # while self._running:
        #     try:
        #         url  = self._get_url() + "/odometry"
        #         resp = requests.get(url, timeout=1)
        #         if resp.ok:
        #             self.data_received.emit(resp.json())
        #     except requests.exceptions.RequestException as e:
        #         self.error_occurred.emit(str(e))

        #     # Sleep in small ticks so stop() is responsive
        #     elapsed = 0.0
        #     tick    = 0.05
        #     while self._running and elapsed < self._interval:
        #         self.msleep(int(tick * 1000))
        #         elapsed += tick
BOXES = [
    ("1", "box1"),
    ("2", "box2"),
    ("3", "box3"),
    ("4", "box4"),
    ("5", "box5"),
    ("6", "box6"),
    ("7", "box7"),
    ("8", "box8"),
]

class BoxesDisplay(QGroupBox):
    def __init__(self, parent=None, get_url=None):
        super().__init__("BOXES", parent)
        self._get_url = get_url
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(8, 4, 8, 4)

        for label, name in BOXES:
            row = QWidget()
            row.setStyleSheet(
                f"background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 3px;"
            )
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 4, 10, 4)

            lbl = QLabel(label)
            lbl.setFont(QFont("Courier New", 11))
            lbl.setStyleSheet(f"color: {COLORS['accent']}; border: none;")

            row_layout.addWidget(lbl)
            row_layout.addStretch()
            layout.addWidget(row)

        layout.addStretch()
    