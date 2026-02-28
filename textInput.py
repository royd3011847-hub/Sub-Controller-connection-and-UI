from header import *
from Theme import *

class TextInput(QLineEdit):
    command_ready = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        #self._build_ui()
        self.setPlaceholderText("Enter command...")
        self.returnPressed.connect(self._emit_command)
        

    def _emit_command(self):
        cmd = self.text().strip()
        if cmd:
            self.command_ready.emit(cmd)
            self.clear()