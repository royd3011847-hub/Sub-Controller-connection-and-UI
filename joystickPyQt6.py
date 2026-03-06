import sys
from header import *
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont


class JoystickWidget(QFrame):
    """Widget to display info for a single joystick."""
    def __init__(self, joystick):
        super().__init__()
        self.joystick = joystick
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        self.labels = {}
        self._build_ui()

    def _make_label(self, key, text=""):
        label = QLabel(text)
        label.setFont(QFont("Courier New", 11))
        self.labels[key] = label
        self.layout_.addWidget(label)
        return label

    def _build_ui(self):
        jid = self.joystick.get_instance_id()
        self._make_label("title", f"Joystick {jid}: {self.joystick.get_name()}")
        self.labels["title"].setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        self._make_label("guid", f"GUID: {self.joystick.get_guid()}")
        self._make_label("axes_header")
        self.axis_labels = []
        for i in range(self.joystick.get_numaxes()):
            lbl = QLabel()
            lbl.setFont(QFont("Courier New", 11))
            self.layout_.addWidget(lbl)
            self.axis_labels.append(lbl)
        self._make_label("buttons_header")
        self.button_labels = []
        for i in range(self.joystick.get_numbuttons()):
            lbl = QLabel()
            lbl.setFont(QFont("Courier New", 11))
            self.layout_.addWidget(lbl)
            self.button_labels.append(lbl)
        self._make_label("hats_header")
        self.hat_labels = []
        for i in range(self.joystick.get_numhats()):
            lbl = QLabel()
            lbl.setFont(QFont("Courier New", 11))
            self.layout_.addWidget(lbl)
            self.hat_labels.append(lbl)

    def refresh(self):
        joy = self.joystick

        for i, lbl in enumerate(self.axis_labels):
            val = joy.get_axis(i)
            if(i == 0):
                lbl.setText(f"  left joystick x axis: {val:>8.4f}")
            if(i == 1):
                lbl.setText(f"  left joystick y axis: {val:>8.4f}")
            if(i == 2):
                lbl.setText(f"  right joystick x axis: {val:>8.4f}")
            if(i == 3):
                lbl.setText(f"  right joystick y axis: {val:>8.4f}")
            if(i == 4):
                lbl.setText(f"  left trigger: {val:>8.4f}")
            if(i == 5):
                lbl.setText(f"  right trigger: {val:>8.4f}")
            lbl.setStyleSheet(
                f"background: {COLORS['bg_card']}; "
            )
       
        for i, lbl in enumerate(self.button_labels):
            val = joy.get_button(i)
            if(i == 0):
                lbl.setText(f"  A button value: \t\t\t{val}")
            if(i == 1):
                lbl.setText(f"  B button value: \t\t\t{val}")
            if(i == 2):
                lbl.setText(f"  X button value: \t\t\t{val}")
            if(i == 3):
                lbl.setText(f"  Y button value: \t\t\t{val}")
            if(i == 4):
                lbl.setText(f"  Disarm button value: \t\t\t{val}")
            if(i == 5):
                lbl.setText(f"  Xbox button value: \t\t\t{val}")
            if(i == 6):
                lbl.setText(f"  Arm button value: \t\t\t{val}")
            if(i == 7):
                lbl.setText(f"  Left joystick button value: \t\t{val}")
            if(i == 8):
                lbl.setText(f"  Right joystick button value: \t\t{val}")
            if(i == 9):
                lbl.setText(f"  Left bumper button value: \t\t{val}")
            if(i == 10):
                lbl.setText(f"  Right bumper button value: \t\t{val}")
            if(i == 11):
                lbl.setText(f"  D-pad up button value: \t\t{val}")
            if(i == 12):
                lbl.setText(f"  D-pad down button value: \t\t{val}")
            if(i == 13):
                lbl.setText(f"  D-pad left button value: \t\t{val}")
            if(i == 14):
                lbl.setText(f"  D-pad right button value: \t\t{val}")
            lbl.setStyleSheet(f"background: {COLORS['bg_card']}; ")



class ControllerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joystick Monitor")
        self.resize(500, 700)

        # --- Outer layout ---
        outer_layout = QVBoxLayout(self)

        self.count_label = QLabel("Number of joysticks: 0")
        self.count_label.setFont(QFont("Courier New", 8, QFont.Weight.Bold))
        outer_layout.addWidget(self.count_label)

        # Scrollable area for joystick widgets
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        outer_layout.addWidget(self.scroll)

        self.scroll_contents = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scroll_contents)

        # --- Pygame init ---
        pygame.init()
        pygame.joystick.init()

        self.joysticks = {}       # instance_id -> Joystick
        self.joy_widgets = {}     # instance_id -> JoystickWidget

        # --- Poll timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll)
        self.timer.start(33)  # ~30 FPS

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                print("hello")
                iid = joy.get_instance_id()
                #if(iid%2==1):
                self.joysticks[iid] = joy
                widget = JoystickWidget(joy)
                self.joy_widgets[iid] = widget
                self.scroll_layout.addWidget(widget)
                print(f"Joystick {iid} connected: {joy.get_name()}")
                    

            elif event.type == pygame.JOYDEVICEREMOVED:
                iid = event.instance_id
                if iid in self.joysticks:
                    del self.joysticks[iid]
                if iid in self.joy_widgets:
                    w = self.joy_widgets.pop(iid)
                    self.scroll_layout.removeWidget(w)
                    w.deleteLater()
                print(f"Joystick {iid} disconnected")

            #BUTTON PRESSED/RELEASED type shit
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed on joystick {event.instance_id}")
                
                # if event.button == 0 and event.instance_id in self.joysticks:
                #     joy = self.joysticks[event.instance_id]
                #     if joy.rumble(0, 0.7, 500):
                #         print(f"Rumble played on joystick {event.instance_id}")

            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released on joystick {event.instance_id}")

        # Update count label
        self.count_label.setText(f"Number of joysticks: {pygame.joystick.get_count()}")

        # Refresh all joystick widgets
        for widget in self.joy_widgets.values():
            widget.refresh()

    def closeEvent(self, event):
        self.timer.stop()
        pygame.quit()
        super().closeEvent(event)
