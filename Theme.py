COLORS = {
    "bg_deep":      "#090d0f",
    "bg_panel":     "#0d1417",
    "bg_card":      "#121c20",
    "bg_input":     "#0a1214",
    "border":       "#1e3038",
    "border_bright":"#2a4855",
    "accent":       "#00ff88",
    "accent_dim":   "#009950",
    "accent_glow":  "#00ff8833",
    "warn":         "#ffaa00",
    "danger":       "#ff3b3b",
    "text_primary": "#d4ede5",
    "text_secondary":"#6a9a8a",
    "text_dim":     "#2e5045",
    "conn_ok":      "#00ff88",
    "conn_bad":     "#ff3b3b",
    "mode_imu":     "#00ccff",
    "mode_script":  "#ff8c00",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_primary']};
    font-family: 'Courier New', 'Lucida Console', monospace;
}}

QGroupBox {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    margin-top: 22px;
    padding: 8px 6px 6px 6px;
    font-size: 10px;
    font-weight: bold;
    color: {COLORS['text_secondary']};
    letter-spacing: 2px;
    text-transform: uppercase;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: {COLORS['bg_deep']};
    border: 1px solid {COLORS['border']};
    border-radius: 2px;
    color: {COLORS['text_secondary']};
    letter-spacing: 3px;
}}

QLineEdit {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 3px;
    color: {COLORS['accent']};
    font-family: 'Courier New', monospace;
    font-size: 20px;
    padding: 4px 8px;
    margin: 5px;
    min-width: 200px;
    selection-background-color: {COLORS['accent_dim']};
}}

QLineEdit:focus {{
    border: 1px solid {COLORS['accent_dim']};
    background-color: #0d1a16;
}}

QLineEdit:disabled {{
    color: {COLORS['text_dim']};
    border-color: {COLORS['text_dim']};
}}

QPushButton {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border_bright']};
    border-radius: 3px;
    color: {COLORS['text_primary']};
    font-family: 'Courier New', monospace;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 7px 16px;
}}

QPushButton:hover {{
    background-color: #162228;
    border-color: {COLORS['accent_dim']};
    color: {COLORS['accent']};
}}

QPushButton:pressed {{
    background-color: #0d1a16;
}}

QPushButton:disabled {{
    color: {COLORS['text_dim']};
    border-color: {COLORS['text_dim']};
}}

QPushButton#btn_send {{
    background-color: #0a2018;
    border: 1px solid {COLORS['accent_dim']};
    color: {COLORS['accent']};
}}

QPushButton#btn_send:hover {{
    background-color: #0f2e22;
    border-color: {COLORS['accent']};
}}

QPushButton#btn_script {{
    background-color: #1a1000;
    border: 1px solid #995500;
    color: {COLORS['mode_script']};
    font-size: 13px;
    padding: 14px 24px;
    letter-spacing: 3px;
}}

QPushButton#btn_script:hover {{
    background-color: #241600;
    border-color: {COLORS['mode_script']};
}}

QPushButton#btn_connect {{
    background-color: #0a1a14;
    border: 1px solid {COLORS['accent_dim']};
    color: {COLORS['accent']};
    letter-spacing: 3px;
}}

QPushButton#btn_disconnect {{
    background-color: #1a0a0a;
    border: 1px solid #882222;
    color: {COLORS['danger']};
    letter-spacing: 3px;
}}

QPushButton#mode_btn {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
    padding: 10px 20px;
    font-size: 12px;
    letter-spacing: 3px;
    border-radius: 0px;
}}

QPushButton#mode_btn:checked {{
    border-bottom: 2px solid {COLORS['accent']};
    color: {COLORS['accent']};
    background-color: #0d1a16;
}}

QCheckBox {{
    color: {COLORS['text_secondary']};
    font-size: 11px;
    spacing: 6px;
}}

QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border: 1px solid {COLORS['border_bright']};
    border-radius: 2px;
    background: {COLORS['bg_input']};
}}

QCheckBox::indicator:checked {{
    background: {COLORS['accent_dim']};
    border-color: {COLORS['accent']};
    image: none;
}}

QTextEdit {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 3px;
    color: {COLORS['text_secondary']};
    font-family: 'Courier New', monospace;
    font-size: 11px;
    padding: 4px;
}}

QScrollBar:vertical {{
    background: {COLORS['bg_deep']};
    width: 6px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['border_bright']};
    border-radius: 3px;
    min-height: 20px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QSplitter::handle {{
    background: {COLORS['border']};
    width: 1px;
}}

QStatusBar {{
    background-color: {COLORS['bg_panel']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
    font-size: 10px;
    letter-spacing: 1px;
}}

QFrame#divider {{
    color: {COLORS['border']};
    background-color: {COLORS['border']};
}}
"""