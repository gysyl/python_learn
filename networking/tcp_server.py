import os
import socket
import threading
import tempfile
from pathlib import Path

# 用于存储服务器端口号的临时文件
SERVER_PORT_FILE = Path(tempfile.gettempdir()) / "tcp_server_port.txt"


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """处理单个客户端连接。使用 with 以确保连接被关闭。"""
    with conn:
        print(f"[server] Connected by {addr}")
        try:
            data = conn.recv(1024)
            if not data:
                print("[server] 客户端未发送数据或已关闭连接")
                return
            # 尝试以 utf-8 解码以便可读输出
            try:
                text = data.decode("utf-8")
                print(f"[server] Received: {text!r}")
            except Exception:
                print(f"[server] Received bytes: {data}")

            # 这里发送一个简短的回复（示例）
            conn.sendall(b"Hello, client!")
            print("[server] 已发送回复，关闭客户端连接")
        except Exception as e:
            print(f"[server] 处理客户端时发生错误: {e}")


def tcp_server(host: str = "127.0.0.1", port: int = 8888) -> None:
    """启动一个简单的多线程 TCP 服务器（每个连接用独立线程处理）。

    这是教学示例，非生产就绪。提供 host/port 参数便于测试。
    默认绑定到 127.0.0.1（回环地址）而不是 localhost，避免解析问题。
    """
    print("[server] 创建套接字...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 避免快速重启时出现"地址已在使用"的错误
        print("[server] 设置 SO_REUSEADDR...")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print(f"[server] 尝试绑定到 {host}:{port}...")
        s.bind((host, port))
        # 获取实际绑定的地址和端口
        actual_port = s.getsockname()[1]
        print(f"[server] 已成功绑定到 {host}:{actual_port}")
        
        # 将实际端口号写入临时文件
        print(f"[server] 保存端口号到 {SERVER_PORT_FILE}...")
        SERVER_PORT_FILE.write_text(str(actual_port))
        
        print("[server] 开始监听，backlog=7...")
        s.listen(7)
        
        print(f"[server] 正在监听 {s.getsockname()}，等待客户端连接...")

        try:
            while True:
                conn, addr = s.accept()
                # 使用线程处理每个客户端，避免单个慢客户端阻塞服务器
                t = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                t.start()
        except KeyboardInterrupt:
            print("[server] 收到中断信号，准备关闭服务器…")
        except Exception as e:
            print(f"[server] 服务器运行时发生错误: {e}")
        finally:
            # 退出 with 会自动关闭 socket
            # 删除端口文件
            if SERVER_PORT_FILE.exists():
                SERVER_PORT_FILE.unlink()
            print("[server] 服务器套接字已关闭（优雅退出）")


def _find_free_port(host: str = "127.0.0.1") -> int:
    """找到一个空闲的端口号。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))  # 让操作系统分配空闲端口
        return s.getsockname()[1]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple TCP server for learning")
    parser.add_argument("--host", default="127.0.0.1", help="监听主机，默认 127.0.0.1")
    parser.add_argument("--port", type=int, help="监听端口，默认自动选择")
    args = parser.parse_args()
    
    if not args.port:
        args.port = _find_free_port(args.host)
    
    tcp_server(args.host, args.port)
    