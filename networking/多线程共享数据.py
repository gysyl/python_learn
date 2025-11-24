"""
需求:定义全局变量my_list=[],定义两个目标函数分别实现添加,查看数据,最后创建两个线程,分别执行对应的任务,观察结果
"""
import threading
import time
import os

my_list = []

def add_data():
    for i in range(5):
        my_list.append(i)
        print(f"[添加线程][pid={os.getpid()}] 添加了 {i} 到列表")
        # time.sleep(1)
    print(f"[添加线程][pid={os.getpid()}] 列表当前状态: {my_list}")

def view_data():
    for item in my_list:
        print(f"[查看线程][pid={os.getpid()}] 列表当前状态: {item}")
        time.sleep(1)

if __name__ == "__main__":
    # 创建两个线程：一个用于添加数据，一个用于查看数据
    add_thread = threading.Thread(target=add_data)
    view_thread = threading.Thread(target=view_data)

    # 启动线程
    add_thread.start()
    view_thread.start()

    # 等待两个线程完成
    add_thread.join()
    view_thread.join()
    print(f"[查看线程][pid={os.getpid()}] 列表当前状态: {my_list}")