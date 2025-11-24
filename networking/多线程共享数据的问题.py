"""
需求: 定义两个函数,分别对全局变量累加 100W 次,创建两个线程,关联这两个函数,执行看效果.

演示目标:
- 无锁情况下会出现竞态条件,最终结果往往小于预期值 2_000_000。
- 加锁 (threading.Lock) 后可得到正确结果,但会牺牲一些性能。
"""
import threading
import time
import os


# 全局计数器 (演示共享数据)
counter = 0
N = 5_000_000
lock = threading.Lock()


def add_no_lock():
    """无锁累加: 可能出现丢失更新"""
    global counter
    for _ in range(N):
        counter += 1
        # 模拟一些耗时操作
        #time.sleep(0.001)

def add_with_lock():
    """加锁累加: 保证操作的原子性"""
    global counter
    for _ in range(N):
        with lock:
            counter += 1


def run_case(target, title):
    """运行一个案例并打印耗时与结果"""
    global counter
    counter = 0
    t1 = threading.Thread(target=target, name=f"{title}-T1")
    t2 = threading.Thread(target=target, name=f"{title}-T2")

    start = time.perf_counter()
    t1.start(); t2.start()
    t1.join(); t2.join()
    dur = time.perf_counter() - start

    expected = 2 * N
    print(
        f"[{title}][pid={os.getpid()}] 期望={expected} 实际={counter} 用时={dur:.3f}s"
    )


if __name__ == "__main__":
    # 案例1: 无锁 (可能小于期望)
    run_case(add_no_lock, "无锁")
    # 案例2: 加锁 (应等于期望)
    run_case(add_with_lock, "加锁")


