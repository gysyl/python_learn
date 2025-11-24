import socket
import tempfile
import time
from pathlib import Path


# 定义服务器端口文件路径（与服务器端保持一致）
SERVER_PORT_FILE = Path(tempfile.gettempdir()) / "tcp_server_port.txt"


# 创建最简单的 tcp 客户端，支持主机/端口/消息参数和基本错误处理
def tcp_client(
    host: str = "127.0.0.1",
    port: int = 8888,
    message: str = "Hello, server!",
    use_port_file: bool = True,
) -> None:
    # 如果启用了端口文件，尝试从文件读取端口
    if use_port_file:
        if not SERVER_PORT_FILE.exists():
            print(f"[client] 端口文件 {SERVER_PORT_FILE} 不存在")
            print("[client] 等待服务器启动（最多等待 10 秒）...")
            for _ in range(10):
                if SERVER_PORT_FILE.exists():
                    break
                time.sleep(1)
        
        if SERVER_PORT_FILE.exists():
            try:
                port = int(SERVER_PORT_FILE.read_text().strip())
                print(f"[client] 从文件读取到服务器端口: {port}")
            except (ValueError, OSError) as e:
                print(f"[client] 读取端口文件失败: {e}")
                print("[client] 使用默认端口...")
        else:
            print("[client] 服务器似乎未启动，使用默认端口...")

    print(f"[client] 准备连接到 {host}:{port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 设置超时，避免阻塞过久
        print("[client] 设置超时为 5 秒...")
        s.settimeout(5)
        
        print(f"[client] 尝试连接 {host}:{port}...")
        s.connect((host, port))
        local_addr = s.getsockname()
        print(f"[client] 已连接到 {host}:{port}，本地地址 {local_addr}")
        
        print(f"[client] 发送消息: {message!r}...")
        s.sendall(message.encode("utf-8"))

        try:
            data = s.recv(1024)
        except TimeoutError:
            print("[client] 接收超时（未收到服务器响应）")
            return

        if data:
            try:
                print(f"[client] Received: {data.decode('utf-8')}")
            except Exception:
                print(f"[client] Received bytes: {data}")

        # 连接会在 with 退出时自动关闭
        print("[client] 即将关闭客户端套接字")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple TCP client for learning")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="服务器主机，默认 127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8888,
        help="服务器端口，默认 8888",
    )
    parser.add_argument(
        "--message",
        default="Hello, server!",
        help="发送的消息，默认 'Hello, server!'",
    )
    parser.add_argument(
        "--no-port-file",
        action="store_true",
        help="不使用端口文件，强制使用命令行指定的端口",
    )
    args = parser.parse_args()

    try:
        tcp_client(
            host=args.host,
            port=args.port,
            message=args.message,
            use_port_file=not args.no_port_file,
        )
    except ConnectionRefusedError:
        print(f"[client] 无法连接到 {args.host}:{args.port}（连接被拒绝）")
    except Exception as e:
        print(f"[client] 运行时错误: {e}")
