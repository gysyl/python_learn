"""
用多进程模拟边编程边听音乐的场景
"""
import multiprocessing
import time

def play_music():
    """模拟播放音乐的函数"""
    for i in range(5):
        print(f"[音乐] 正在播放第 {i + 1} 首歌...")
        time.sleep(1)  # 模拟每首歌播放时间
def coding():
    """模拟编程的函数"""
    for i in range(5):
        print(f"[编程] 正在编写第 {i + 1} 行代码...")
        time.sleep(1.5)  # 模拟编写代码时间
        
if __name__ == "__main__":
    # 创建两个进程：一个用于播放音乐，一个用于编程
    music_process = multiprocessing.Process(target=play_music)
    coding_process = multiprocessing.Process(target=coding)

    # 启动进程
    music_process.start()
    coding_process.start()

    # 等待两个进程完成
    music_process.join()
    coding_process.join()

    print("音乐播放和编程任务已完成。")