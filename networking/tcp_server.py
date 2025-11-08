import socket

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 避免快速重启时出现“地址已在使用”的错误
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", 8888))
        print("[server] 已绑定到 localhost:8888")
        s.listen(7)
        print("[server] 正在监听，backlog=7；等待客户端连接…")

        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"[server] Connected by {addr}")
                    data = conn.recv(1024)
                    if data:
                        print(f"[server] Received bytes: {data}")
                        conn.sendall(b"Hello, client!")
                        print("[server] 已发送回复，关闭客户端连接")
                    else:
                        print("[server] 客户端未发送数据，关闭连接")
        except KeyboardInterrupt:
            print("[server] 收到中断信号，准备关闭服务器…")
        except Exception as e:
            print(f"[server] 服务器运行时发生错误: {e}")
        finally:
            # 退出 with 会自动关闭 socket
            print("[server] 服务器套接字已关闭（优雅退出）")


if __name__ == "__main__":
    tcp_server()
    