from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSlider

# Only needed for access to command line arguments
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__() # Call the parent constructor
        self.setWindowTitle("wow it works!")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: lightblue;")

        layout = QVBoxLayout(self)

        self.label = QLabel("<h1>Hello, PyQt6!</h1>", parent=self)
        self.button = QPushButton("Click me!", parent=self)
        self.button.clicked.connect(self.on_button_click)

        self.slider = QSlider(parent=self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.slider)

    def on_button_click(self):
        self.label.setText("<h1>Button Clicked!</h1>")
        print(self.slider.value())
        self.button.setText("Clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())