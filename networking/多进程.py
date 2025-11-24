"""
用多进程模拟边编程边听音乐的场景

修复点：
- Process.start() 不接受参数；应在构造 Process 时通过 args 传参。
- 函数参数语义明确：使用 count 表示循环次数，避免与循环变量重名。
"""
import multiprocessing
import os
import time


def play_music(name: str, count: int) -> None:
    """模拟播放音乐的函数"""
    for idx in range(count):
        print(f"[音乐][pid={os.getpid()}] {name} 正在播放第 {idx + 1} 首歌...")
        time.sleep(1)  # 模拟每首歌播放时间
    print(f"[音乐的进程是：{os.getpid()}],[音乐的父进程是：{os.getppid()}]。")

def coding(name: str, lines: int) -> None:
    """模拟编程的函数"""
    for idx in range(lines):
        print(f"[编程][pid={os.getpid()}] {name} 正在编写第 {idx + 1} 行代码...")
        time.sleep(1.5)  # 模拟编写代码时间
    print(f"[编程的进程是：{os.getpid()}],[编程的父进程是：{os.getppid()}]。")

if __name__ == "__main__":
    # Windows 上推荐使用 spawn 以保证兼容交互/IDE环境
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        # 已设置过启动方式则忽略
        pass

    # 创建两个进程：一个用于播放音乐，一个用于编程
    music_process = multiprocessing.Process(
        target=play_music, args=("音乐进程", 5), name="MusicProc"
    )
    coding_process = multiprocessing.Process(
        target=coding, args=("编程进程", 5), name="CodingProc"
    )

    # 启动进程（start 不接收额外参数）
    music_process.start()
    coding_process.start()

    # 等待两个进程完成
    music_process.join()
    coding_process.join()

    print("音乐播放和编程任务已完成。")