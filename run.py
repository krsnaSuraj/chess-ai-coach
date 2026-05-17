"""
Chess Coach - Launcher
Usage:
  python run.py          -> Start Desktop GUI (default)
  python run.py desktop  -> Start Desktop GUI
  python run.py web      -> Start Web Server (http://localhost:8000)
  python run.py web 8080 -> Start Web Server on port 8080
"""

import sys
import os
import socket

def main():
    args = [a.lower() for a in sys.argv[1:]]
    mode = "desktop"

    if "web" in args or "server" in args or "--web" in args:
        mode = "web"
    elif "-h" in args or "--help" in args or len(args) > 2:
        print(__doc__)
        return

    if mode == "desktop":
        from PyQt6.QtWidgets import QApplication
        from board_gui import MainWindow

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    else:
        import uvicorn
        from server import app

        port = 8000
        for a in args:
            if a.isdigit():
                port = int(a)
                break

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("0.0.0.0", port))
            sock.close()
        except OSError:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("0.0.0.0", 0))
            port = sock.getsockname()[1]
            sock.close()

        local_ip = "127.0.0.1"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        print()
        print("=" * 50)
        print("  Chess Coach Web Server is running!")
        print("=" * 50)
        print(f"  PC:  http://localhost:{port}")
        print(f"  Phone:  http://{local_ip}:{port}")
        print("=" * 50)
        print(f"  Phone not working? Make sure:")
        print(f"  1. Phone is on the SAME WiFi as this PC")
        print(f"  2. Windows Firewall allows port {port}")
        print(f"     -> Run this in PowerShell (as admin):")
        print(f'     New-NetFirewallRule -DisplayName "Chess Coach" -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow')
        print("=" * 50)
        print()
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


if __name__ == "__main__":
    main()
