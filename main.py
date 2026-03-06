"""
Robotic Submarine Controller
PyQt6-based ground control station
Communicates with sub over Ethernet
"""


from Connection import * 
from IMUDisplay import *
from controllerPanel import *
from header import *
from joystickPyQt6 import ControllerWindow
from logPanel import *
from textInput import *


# main windows
class SubmarineController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TIGER FISH LETS GOOOO!!!")
        self.resize(1200, 820)
        self.setMinimumSize(900, 640)

        self._worker: ConnectionWorker | None = None

        self._build_ui()
        self.setStyleSheet(STYLESHEET)

    # ── UI BUILD ──────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(10, 10, 10, 6)
        root.setSpacing(8)

        # ── CONNECTION BAR ───────────────────
        conn_bar = QWidget()
        conn_bar.setMaximumHeight(100)
        conn_bar.setStyleSheet(
            f"background: {COLORS['bg_panel']}; border: 1px solid {COLORS['border']}; border-radius: 4px;"
        )
        conn_layout = QHBoxLayout(conn_bar)
        conn_layout.setContentsMargins(12, 8, 12, 8)
        conn_layout.setSpacing(10)

        def _field_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet(
                f"color: {COLORS['text_secondary']}; font-size: 10px; "
                f"letter-spacing: 2px; border: none; background: transparent;"
            )
            return lbl

        conn_layout.addWidget(_field_label("HOST"))
        self._host_input = QLineEdit("192.168.1.100")
        self._host_input.setFixedWidth(150)
        self._host_input.setFixedHeight(50)
        conn_layout.addWidget(self._host_input)

        conn_layout.addSpacing(8)

        self._btn_connect = QPushButton("CONNECT")
        self._btn_connect.setObjectName("btn_connect")
        self._btn_connect.setFixedHeight(40)
        self._btn_connect.clicked.connect(self._connect)
        conn_layout.addWidget(self._btn_connect)

        conn_layout.addSpacing(8)
        
        # vertical divider
        vdiv = QFrame()
        vdiv.setFrameShape(QFrame.Shape.VLine)
        vdiv.setFixedWidth(1)
        vdiv.setStyleSheet(f"background: {COLORS['border']}; border: none;")
        conn_layout.addWidget(vdiv)
        
        conn_layout.addSpacing(8)
        
        # KILL button
        self._btn_kill = QPushButton("KILL")
        self._btn_kill.setFixedHeight(70)
        
        conn_layout.addWidget(self._btn_kill)
        self._btn_kill.setStyleSheet(
            f"background: #2a0000; border: 1px solid {COLORS['danger']}; "
            f"color: {COLORS['danger']}; font-size: 11px; font-weight: bold; "
            f"letter-spacing: 3px; padding: 0px 14px; border-radius: 3px;"  
        )
        self._btn_kill.setToolTip("Immediately power off the submarine")
        self._btn_kill.clicked.connect(self._kill_sub)
        conn_layout.addWidget(self._btn_kill, 2)

        conn_layout.addStretch()
        root.addWidget(conn_bar)

        # ── MAIN CONTENT SPLITTER ─────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setChildrenCollapsible(False)

        # LEFT: mode control
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 4, 0)
        left_layout.setSpacing(8)


        # Stacked pages
        self._stack = QStackedWidget()

        
        # -- Controller page
        self._controller_panel = ControllerWindow()

        left_layout.addWidget(self._controller_panel)
        
        
        # RIGHT: telemetry display
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(4, 0, 0, 0)
        right_layout.setSpacing(8)

        self._telemetry = TelemetryDisplay()
        right_layout.addWidget(self._telemetry)
        
        # Log
        self._log = LogPanel()
        right_layout.addWidget(self._log)
        

        splitter.addWidget(left)

        # Timestamp of last packet
        self._last_update_lbl = QLabel("LAST UPDATE: ——")
        self._last_update_lbl.setStyleSheet(
            f"color: {COLORS['text_dim']}; font-size: 9px; letter-spacing: 2px;"
        )
        right_layout.addWidget(self._last_update_lbl)
        right_layout.addStretch()

        splitter.addWidget(right)
        splitter.setSizes([700, 480])

        root.addWidget(splitter)

        # ── STATUS BAR ───────────────────────
        sb = QStatusBar()
        self.setStatusBar(sb)
        
        
         # -- terminal / input box
        self._text_input = TextInput()
        self._text_input.command_ready.connect(self._on_command)
        sb.addPermanentWidget(self._text_input, 1)


    # ── CONNECT / DISCONNECT ──────────────────
    def _connect(self):
        host = self._host_input.text().strip()
        host = self._host_input.text().strip()
        self._worker = ConnectionWorker(host)
        self._log.append(f"Connecting to {host}...", "info")
    
    def _kill_sub(self):
        payload = {"mode": "kill"}
        self._log.append("KILL SIGNAL SENT — submarine powering off", "err")
        if self._worker:
            self._worker.send(payload)

    # ── COMMAND SEND ──────────────────────────
    def _on_command(self, payload: dict):
        # If command came from TextInput, it's a string
        if isinstance(payload, str):
            cmd = payload.strip()

            # local command
            if cmd == "clear":
                self.clear_log()
                return

            # convert to structured dict for sending
            payload = {"command": cmd}

        msg = json.dumps(payload)
        self._log.append(f"command → {msg}", "send")

        if self._worker:
            self._worker.send(payload)

    # ── TELEMETRY RECEIVE ─────────────────────
    def _on_telemetry(self, data: dict):
        self._telemetry.update_values(data)
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self._last_update_lbl.setText(f"LAST UPDATE: {ts}")
        
    def clear_log(self):
        self._log.clear()
        
    def _controller_connected(self):
        self._log.append("Controller connected", "info")
        

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Sub Control Station")

    # Dark palette safety net
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,      QColor(COLORS["bg_deep"]))
    palette.setColor(QPalette.ColorRole.WindowText,  QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.Base,        QColor(COLORS["bg_input"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS["bg_panel"]))
    palette.setColor(QPalette.ColorRole.Text,        QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.Button,      QColor(COLORS["bg_card"]))
    palette.setColor(QPalette.ColorRole.ButtonText,  QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.Highlight,   QColor(COLORS["accent_dim"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS["bg_deep"]))
    app.setPalette(palette)

    window = SubmarineController()
    window.show()
    sys.exit(app.exec())
    


if __name__ == "__main__":
    main()