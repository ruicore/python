import concurrent.futures

import time


def sample(seconds: int):
    time.sleep(seconds)
    print(f"wait for {seconds}")
    return seconds


if __name__ == '__main__':
    start = time.perf_counter()
    seconds = [5, 4, 3, 2, 1]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # executor.map()
        results = [executor.submit(sample, sec) for sec in seconds]
        for f in results:
            print(f.result())
    end = time.perf_counter()
    print(end - start)
