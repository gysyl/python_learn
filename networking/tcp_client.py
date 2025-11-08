import socket
# 创建最简单的tcp客户端，只需单次连接
def tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 8888))
        print("[client] 已连接到 localhost:8888")
        s.sendall(b"Hello, server!")
        data = s.recv(1024)
        # 解码输出更易读
        try:
            print(f"[client] Received: {data.decode('utf-8')}")
        except Exception:
            print(f"[client] Received bytes: {data}")
        # 连接会在 with 退出时自动关闭
        print("[client] 即将关闭客户端套接字")
if __name__ == "__main__":
    tcp_client()
        