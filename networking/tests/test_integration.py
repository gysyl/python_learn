import multiprocessing
import socket
import time

from networking.tcp_server import tcp_server


def _find_free_port(host: str = "127.0.0.1") -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_server_client_integration():
    """启动服务器子进程，用 socket 连接并断言收到预期回复。"""
    host = "127.0.0.1"
    port = _find_free_port(host)

    proc = multiprocessing.Process(target=tcp_server, args=(host, port), daemon=True)
    proc.start()

    # 等待服务器启动并监听
    time.sleep(0.2)

    try:
        with socket.create_connection((host, port), timeout=2) as conn:
            conn.sendall(b"ping")
            data = conn.recv(1024)

        assert data == b"Hello, client!"
    finally:
        # 尽量清理子进程
        if proc.is_alive():
            proc.terminate()
            proc.join(timeout=1)
