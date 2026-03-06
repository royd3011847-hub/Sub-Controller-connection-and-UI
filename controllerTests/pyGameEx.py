import sys
import pygame
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer

class ControllerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controller Test")
        self.label = QLabel("Waiting for controller...")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        pygame.init()
        pygame.joystick.init()

        self.joysticks = {}  # instance_id -> Joystick

        # Register any already-connected joysticks
        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            self.joysticks[joy.get_instance_id()] = joy
            print("Connected:", joy.get_name())

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_controller)
        self.timer.start(16)

    def poll_controller(self):
        # ✅ Process ALL events — including hotplug
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                self.label.setText(f"Controller connected: {joy.get_name()}")
                print("Connected:", joy.get_name())

            if event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in self.joysticks:
                    del self.joysticks[event.instance_id]
                self.label.setText("Controller disconnected.")
                print("Disconnected:", event.instance_id)

        if not self.joysticks:
            return

        # Check first available joystick
        joystick = next(iter(self.joysticks.values()))

        if joystick.get_button(0):
            self.label.setText("Button A Pressed")
        else:
            self.label.setText("Waiting for input...")

app = QApplication(sys.argv)
window = ControllerWindow()
window.show()
sys.exit(app.exec())