"""
player_app.py

Main entry point for the Player application.
Displays Gandor Chat Feed, Initiative Order, Session Log, and Active Table.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel
)
from network_client import NetworkClient


class PlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackstone Codex – Player App")
        self.resize(800, 600)
        self.setup_ui()

        self.network_client = NetworkClient()
        self.network_client.register_hook("gandor_chat", self.receive_gandor_message)
        self.network_client.start()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Top panels
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        self.gandor_feed = QTextEdit()
        self.gandor_feed.setReadOnly(True)
        self.gandor_feed.setPlaceholderText("Gandor Chat Feed")
        top_layout.addWidget(self._wrap_with_label("Gandor Chat Feed", self.gandor_feed))

        self.initiative_order = QTextEdit()
        self.initiative_order.setReadOnly(True)
        self.initiative_order.setPlaceholderText("Initiative Order")
        top_layout.addWidget(self._wrap_with_label("Initiative Order", self.initiative_order))

        # Bottom panels
        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self.session_log = QTextEdit()
        self.session_log.setReadOnly(True)
        self.session_log.setPlaceholderText("Session Log")
        bottom_layout.addWidget(self._wrap_with_label("Session Log", self.session_log))

        self.active_table = QTextEdit()
        self.active_table.setReadOnly(True)
        self.active_table.setPlaceholderText("Active Table")
        bottom_layout.addWidget(self._wrap_with_label("Active Table", self.active_table))

    def _wrap_with_label(self, title, widget):
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout()
        wrapper.setLayout(wrapper_layout)
        wrapper_layout.addWidget(QLabel(title))
        wrapper_layout.addWidget(widget)
        return wrapper

    def receive_gandor_message(self, payload):
        text = payload.get("text", "")
        self.gandor_feed.append(text)
        self.session_log.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayerWindow()
    window.show()
    sys.exit(app.exec())
