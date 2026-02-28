from header import *
from Theme import *




class ConnectionWorker(QObject):
    connected = pyqtSignal()
    

    def __init__(self, host=""):
        super().__init__()
        self._host = host
        print("trying to connect to", host)
        
        
        
