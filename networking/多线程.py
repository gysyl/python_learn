"""
用多线程模拟边编程边听音乐的场景
"""
import threading
import time
import os


def play_music(name, count):
    """模拟播放音乐的函数"""
    for idx in range(count):
        print(
            f"[音乐][thread={threading.current_thread().name}] {name} 正在播放第 {idx + 1} 首歌..."
        )
        time.sleep(1)  # 模拟每首歌播放时间


def coding(name, lines):
    """模拟编程的函数"""
    for idx in range(lines):
        print(
            f"[编程][pid={os.getpid()}][thread={threading.current_thread().name}] {name} 正在编写第 {idx + 1} 行代码..."
        )
        time.sleep(1.5)  # 模拟编写代码时间


if __name__ == "__main__":
    # 线程不需要设置 start method；直接创建并启动即可
    # 创建两个线程：一个用于播放音乐，一个用于编程
    music_thread = threading.Thread(
        target=play_music, args=("音乐线程", 5), name="MusicThread"
    )
    coding_thread = threading.Thread(
        target=coding, args=("编程线程", 5), name="CodingThread"
    )

    # 启动线程
    music_thread.start()
    coding_thread.start()

    # 等待两个线程完成
    music_thread.join()
    coding_thread.join()
    print(
        f"[主进程 pid={os.getpid()}] 音乐与编程任务已完成。"
    )