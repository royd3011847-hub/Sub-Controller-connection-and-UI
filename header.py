

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QLineEdit, QGroupBox,
    QStackedWidget, QCheckBox, QSplitter, QFrame, QScrollArea,
    QTextEdit, QSizePolicy, QSpacerItem, QStatusBar
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QObject, QPropertyAnimation,
    QEasingCurve, QRect, pyqtProperty, QProcess
)
from PyQt6.QtGui import (
    QFont, QFontDatabase, QPalette, QColor, QPainter, QPen,
    QBrush, QLinearGradient, QPixmap, QIcon
)
import sys
import json
import socket
from datetime import datetime
import pygame
from Theme import *