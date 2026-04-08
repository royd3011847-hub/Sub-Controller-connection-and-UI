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
    ("box 1", "box1"),
    ("box 2", "box2"),
    ("box 3", "box3"),
    ("box 4", "box4"),
    ("box 5", "box5"),
    ("box 6", "box6")
]

class BoxesDisplay(QGroupBox):
    def __init__(self, parent=None, get_url=None):
        super().__init__("BOXES", parent)
        self._get_url = get_url
        self._labels = {}
        self._build_ui()

    def _build_ui(self):

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)
        
        for label, name in BOXES:
            cell = QWidget()
            cell.setStyleSheet(
            f"background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 3px;"
            )
            cell.setMinimumHeight(30)
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(4, 2, 4, 2)
            cell_layout.setSpacing(1)
            
            
            name_lbl = QLabel(label)
            name_lbl.setFont(QFont("Courier New", 12))
            name_lbl.setStyleSheet(f"color: {COLORS['text_dim']}; border: none;")
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            val_lbl = QLabel("——")
            val_lbl.setFont(QFont("Courier New", 15))
            val_lbl.setStyleSheet(f"color: {COLORS['accent']}; border: none;")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl.setMinimumWidth(60)
            
            cell_layout.addWidget(name_lbl)
            cell_layout.addWidget(val_lbl)
            layout.addWidget(cell)
            
            self._labels[name] = val_lbl
            
       

        

    def set_value(self, name: str, value):
        if name in self._labels:
            self._labels[name].setText(str(value) if value is not None else "-")
    