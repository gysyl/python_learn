from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_in_threads(func: Callable, items: Iterable, max_workers: int = 4) -> list:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(func, x): x for x in items}
        for fut in as_completed(futures):
            results.append(fut.result())
    return results


if __name__ == "__main__":
    print(run_in_threads(lambda x: x * x, range(5)))
