from header import *

# Background Pulling worker
class BoxesWorker(QThread):
    data_received  = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, get_url_fn, interval: float = 0.1):
        super().__init__()
        self._get_url  = get_url_fn
        self._interval = interval
        self._running  = True
    
    def run(self):
        while self._running:
            try:
                url  = self._get_url() + "/boxes_get"
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
        
# total number of boxes


class BoxesDisplay(QGroupBox):
    def __init__(self, boxes, parent=None, get_url=None):
        super().__init__("BOXES", parent)
        self.boxes = boxes
        self.get_url = get_url
        # numeric value in each box
        self._values = {}
        # string title of each box
        self._titles = {}
        self._build_ui()
        self.running = True
        
        self._worker = None
        if callable(self.get_url):
            self._start_worker()

    def _start_worker(self):
        self._worker = BoxesWorker(self.get_url)
        self._worker.data_received.connect(self.update_values)
        self._worker.error_occurred.connect(lambda err: print(f"Box worker error: {err}"))
        self._worker.start()
        
    def set_url_provider(self, get_url_fn):
        self.get_url = get_url_fn
        if self._worker is None:
            self._start_worker()    
            
    def stop_worker(self):
        """Call from the parent window's closeEvent."""
        if self._worker:
            self._worker.stop()

    def _build_ui(self):

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(10, 5, 10, 5)
        self._layout.setSpacing(8)
        
        for i in range(self.boxes):
            # the box itself
            cell = QWidget()
            cell.setStyleSheet(
                f"background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 3px;"
            )
            cell.setMinimumHeight(30)
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(4, 2, 4, 2)
            cell_layout.setSpacing(1)
            
            # title in the box
            name_lbl = QLabel("——")
            name_lbl.setFont(QFont("Courier New", 12))
            name_lbl.setStyleSheet(f"color: {COLORS['text_dim']}; border: none;")
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_lbl.setMinimumWidth(60)

            # value in the box
            val_lbl = QLabel("——")
            val_lbl.setFont(QFont("Courier New", 15))
            val_lbl.setStyleSheet(f"color: {COLORS['accent']}; border: none;")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl.setMinimumWidth(60)

            cell_layout.addWidget(name_lbl)
            cell_layout.addWidget(val_lbl)
            self._layout.addWidget(cell)

            # This is how we reference each box
            self._titles[i] = name_lbl
            self._values[i] = val_lbl

            # for name, lbl in self._values.items():
            #     print(f"Registered box label: {name} -> {lbl}")
            
    def update_values(self, data: dict):
        for i, box in enumerate(data.get("boxes", [])):
            if i >= self.boxes:
                break
            name  = box.get("Name")
            value = box.get("Value")

            self._titles[i].setText(str(name) if name else "——")
            self._values[i].setText(
                f"{value:+.3f}" if isinstance(value, float) else str(value) if value is not None else "——"
            )

            
# format
"""     
boxesDict = {
    {
        "BoxID" : 1,
        "Name" : "depth",
        "Value": 12
    },
    {
        "BoxID": 1,
        "Name": "heading",
        "Value": 90
    },
    {
        "BoxID": 1,
        "Name": "speed",
        "Value": 3.5
    }
}
"""