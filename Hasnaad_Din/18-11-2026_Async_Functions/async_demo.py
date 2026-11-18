# 18-11-2026_Async_Functions_Din (#104)  # added by Din
# Concurrency vs parallelism demo  # added by Din
# CONCURRENCY = one worker juggling many waiting tasks (asyncio, single core)  # added by Din
# PARALLELISM = many workers doing tasks at the same time (several CPU cores)  # added by Din

import asyncio  # added by Din
import time  # added by Din
from concurrent.futures import ProcessPoolExecutor  # added by Din

import aiohttp  # added by Din


# ---------- Part 1: async def / await ----------  # added by Din
# [ASYNC DEF / AWAIT] async def makes a pausable function; await pauses it while waiting  # added by Din
async def fake_download(name, seconds):  # added by Din
    print(f"Start {name}")  # added by Din
    await asyncio.sleep(seconds)  # added by Din
    print(f"Done  {name} after {seconds}s")  # added by Din
    return name  # added by Din


# [ASYNC DEF / AWAIT] NOT concurrent: each await finishes before the next one starts (3 x 1s = 3s)  # added by Din
async def one_by_one():  # added by Din
    start = time.perf_counter()  # added by Din
    await fake_download("file1", 1)  # added by Din
    await fake_download("file2", 1)  # added by Din
    await fake_download("file3", 1)  # added by Din
    print(f"One by one took {time.perf_counter() - start:.2f}s\n")  # added by Din


# ---------- Part 2: asyncio.gather ----------  # added by Din
# [ASYNCIO.GATHER] CONCURRENCY: starts all 3 together, the waits overlap (about 1s total)  # added by Din
async def all_together():  # added by Din
    start = time.perf_counter()  # added by Din
    results = await asyncio.gather(  # added by Din
        fake_download("file1", 1),  # added by Din
        fake_download("file2", 1),  # added by Din
        fake_download("file3", 1),  # added by Din
    )  # added by Din
    print(f"Results: {results}")  # added by Din
    print(f"gather took {time.perf_counter() - start:.2f}s\n")  # added by Din


# ---------- Part 3: aiohttp + basic loop ----------  # added by Din
URLS = [  # added by Din
    "https://www.python.org",  # added by Din
    "https://pypi.org",  # added by Din
    "https://github.com",  # added by Din
]  # added by Din


# [AIOHTTP] CONCURRENCY: async web request; while waiting for the website, other requests run  # added by Din
async def fetch_url(session, url):  # added by Din
    async with session.get(url) as response:  # added by Din
        text = await response.text()  # added by Din
        print(f"{url} -> status {response.status}, {len(text)} characters")  # added by Din
        return response.status  # added by Din


# [AIOHTTP] + [BASIC LOOP] + [ASYNCIO.GATHER] CONCURRENCY: loop builds the task list, gather runs them together  # added by Din
async def fetch_all():  # added by Din
    start = time.perf_counter()  # added by Din
    async with aiohttp.ClientSession() as session:  # added by Din
        tasks = []  # added by Din
        # [BASIC LOOP] one task per URL  # added by Din
        for url in URLS:  # added by Din
            tasks.append(fetch_url(session, url))  # added by Din
        statuses = await asyncio.gather(*tasks)  # added by Din
    print(f"Statuses: {statuses}")  # added by Din
    print(f"aiohttp fetched {len(URLS)} URLs in {time.perf_counter() - start:.2f}s\n")  # added by Din


# ---------- Part 4: parallelism ----------  # added by Din
# [BASIC LOOP] CPU-heavy work: no waiting, just maths, so asyncio cannot speed it up  # added by Din
def heavy_sum(n):  # added by Din
    total = 0  # added by Din
    for i in range(n):  # added by Din
        total += i * i  # added by Din
    return total  # added by Din


# [PARALLELISM] ProcessPoolExecutor runs heavy_sum on several CPU cores at the same time  # added by Din
def compare_parallel():  # added by Din
    numbers = [5_000_000, 5_000_000, 5_000_000, 5_000_000]  # added by Din

    # NOT parallel: one core does the 4 jobs one after another  # added by Din
    start = time.perf_counter()  # added by Din
    for n in numbers:  # added by Din
        heavy_sum(n)  # added by Din
    print(f"CPU work one by one took {time.perf_counter() - start:.2f}s")  # added by Din

    # [PARALLELISM] each job goes to its own process / CPU core  # added by Din
    start = time.perf_counter()  # added by Din
    with ProcessPoolExecutor() as pool:  # added by Din
        list(pool.map(heavy_sum, numbers))  # added by Din
    print(f"CPU work in parallel took {time.perf_counter() - start:.2f}s")  # added by Din


# ---------- Run everything ----------  # added by Din
# [ASYNC DEF / AWAIT] main is the one async function that runs all the parts in order  # added by Din
async def main():  # added by Din
    print("=== Part 1: one by one ===")  # added by Din
    await one_by_one()  # added by Din
    print("=== Part 2: asyncio.gather (concurrency) ===")  # added by Din
    await all_together()  # added by Din
    print("=== Part 3: aiohttp + loop (concurrency) ===")  # added by Din
    await fetch_all()  # added by Din


if __name__ == "__main__":  # added by Din
    # [ASYNCIO EVENT LOOP] asyncio.run starts the event loop, runs main, then closes the loop  # added by Din
    asyncio.run(main())  # added by Din
    print("=== Part 4: ProcessPoolExecutor (parallelism) ===")  # added by Din
    compare_parallel()  # added by Din