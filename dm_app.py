"""
dm_app.py

Main entry point for the Dungeon Master (DM) application.
It initializes core modules, including the GandorPanel and NetworkServer.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from gandor_panel import GandorPanel
from network_server import NetworkServer

class DMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackstone Codex – DM App")
        self.resize(800, 600)

        # Start network server first
        self.network_server = NetworkServer()
        self.network_server.start_in_thread()

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Hook GandorPanel to broadcast via network
        self.gandor_panel = GandorPanel(hook_manager=self)
        layout.addWidget(self.gandor_panel)

    def trigger_hook(self, hook_name, payload):
        if hook_name == "gandor_chat":
            # Send to player app
            self.network_server.broadcast("gandor_chat", payload)
        else:
            print(f"[HOOK DEBUG] Unknown hook '{hook_name}'")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DMApp()
    window.show()
    sys.exit(app.exec())
