import socket
import threading
import time

import uvicorn
import webview

from app.main import app

HOST = "127.0.0.1"


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def run_server(port: int):
    uvicorn.run(app, host=HOST, port=port, log_level="warning")


def main():
    port = find_free_port()
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(1)

    webview.create_window(
        "Video Downloader",
        f"http://{HOST}:{port}/ui",
        width=560,
        height=420,
        resizable=True,
    )
    webview.start()


if __name__ == "__main__":
    main()
