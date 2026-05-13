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
        import uvicorn, socket
        from server import app

        port = 8000
        for a in args:
            if a.isdigit():
                port = int(a)
                break

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print()
        print("=" * 50)
        print("  Chess Coach Web Server is running!")
        print("=" * 50)
        print(f"  PC:  http://localhost:{port}")
        print(f"  Phone:  http://{local_ip}:{port}")
        print("=" * 50)
        print("  Paste the Phone URL in your mobile browser")
        print("=" * 50)
        print()
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


if __name__ == "__main__":
    main()
