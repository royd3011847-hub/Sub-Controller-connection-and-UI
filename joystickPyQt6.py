import sys
import requests
from header import *
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import json

#this file is for everything controller inputs


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
        self.base_url = None
        self.setWindowTitle("Joystick Monitor")
        self.resize(500, 700)

        self.inputDict = {        # <-- add this
            "x_left_stick": 0.0,
            "y_left_stick": 0.0,
            "x_right_stick": 0.0,
            "y_right_stick": 0.0,

            "a_button": False,
            "b_button": False,
            "x_button": False,
            "y_button": False,

            "up_dpad": False,
            "right_dpad": False,
            "down_dpad": False,
            "left_dpad": False,

            "r_bumper": False,
            "l_bumper": False,
            "r_trigger": 0.0,
            "l_trigger": 0.0
        }
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
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # --- Pygame init ---
        pygame.init()
        pygame.joystick.init()

        self.joysticks = {}       # instance_id -> Joystick
        self.joy_widgets = {}     # instance_id -> JoystickWidget

        # --- Poll timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll)
        self.timer.start(33)  # ~30 FPS
    
    def set_base_url(self, url):
        self.base_url = url

    def poll(self):
        #print(json.dumps(self.inputDict, indent=2)) 
        
        if self.base_url:      # <-- only send if connected
            try:
                requests.post(self.base_url + "/controller_input", json=self.inputDict, timeout=1)
            except requests.exceptions.RequestException:
                print("Failed to send controller input to: " + self.base_url)
                pass
            

        
        for event in pygame.event.get():
                
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                iid = joy.get_instance_id()
                if(joy.get_axis(5) != 0.0):
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
            
                if(0 == event.button):
                    self.inputDict["a_button"] = True
                elif(1 == event.button):
                    self.inputDict["b_button"] = True
                elif(2 == event.button):
                    self.inputDict["x_button"] = True
                elif(3 == event.button):
                    self.inputDict["y_button"] = True
                elif(9 == event.button):
                    self.inputDict["l_bumper"] = True
                elif(10 == event.button):
                    self.inputDict["l_bumper"] = True
                elif(11 == event.button):
                    self.inputDict["up_dpad"] = True
                elif(12 == event.button):
                    self.inputDict["down_dpad"] = True
                elif(13 == event.button):
                    self.inputDict["left_dpad"] = True
                elif(14 == event.button):
                    self.inputDict["right_dpad"] = True
                else:
                    print(f"Button {event.button} pressed on joystick {event.instance_id} not mapped to inputDict")
                

            elif event.type == pygame.JOYBUTTONUP:

                if(0 == event.button):
                    self.inputDict["a_button"] = False
                elif(1 == event.button):
                    self.inputDict["b_button"] = False
                elif(2 == event.button):
                    self.inputDict["x_button"] = False
                elif(3 == event.button):
                    self.inputDict["y_button"] = False
                elif(9 == event.button):
                    self.inputDict["l_bumper"] = False
                elif(10 == event.button):
                    self.inputDict["l_bumper"] = False
                elif(11 == event.button):
                    self.inputDict["up_dpad"] = False
                elif(12 == event.button):
                    self.inputDict["down_dpad"] = False
                elif(13 == event.button):
                    self.inputDict["left_dpad"] = False
                elif(14 == event.button):
                    self.inputDict["right_dpad"] = False
                else:
                    print(f"Button {event.button} released on joystick {event.instance_id} not mapped to inputDict")
                    
            elif event.type == pygame.JOYAXISMOTION:
                
                if(0 == event.axis):
                    self.inputDict["x_left_stick"] = event.value
                elif(1 == event.axis):
                    self.inputDict["y_left_stick"] = event.value
                elif(2 == event.axis):
                    self.inputDict["x_right_stick"] = event.value
                elif(3 == event.axis):
                    self.inputDict["y_right_stick"] = event.value
                elif(4 == event.axis):
                    self.inputDict["l_trigger"] = event.value
                elif(5 == event.axis):
                    self.inputDict["r_trigger"] = event.value
                else:
                    print(f"Axis {event.axis} moved to {event.value:.3f} on joystick {event.instance_id} not mapped to inputDict")

        # Update count label
        self.count_label.setText(f"Number of joysticks: {pygame.joystick.get_count()}")

        # Refresh all joystick widgets
        for widget in self.joy_widgets.values():
            widget.refresh()

    def closeEvent(self, event):
        self.timer.stop()
        pygame.quit()
        super().closeEvent(event)
