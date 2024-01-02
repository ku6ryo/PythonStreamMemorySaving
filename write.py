import psutil
import os
import tempfile

TEN_GB = 10 * 1024 ** 3

def get_memory_usage() -> float:
    process = psutil.Process(os.getpid())
    m = process.memory_info()
    return m.rss / 1024 ** 2

def print_memory_usage(label: str = 'Memory usage'):
    m = get_memory_usage()
    print(f'{label}: {m:.1f} MB')

def write_at_once(size: int):
    with tempfile.TemporaryFile('wb') as f:
        b = b'x' * size
        f.write(b)
        print_memory_usage('Data is hold in memory')

def write_pieces(size: int, chunk_size: int):
    n = size // chunk_size
    print_memory_usage(f'Before chunked writing. {n} chunks')
    memory_usages = []
    with tempfile.TemporaryFile('wb') as f:
        for _ in range(n):
            b = b'x' * chunk_size
            f.write(b)
            memory_usages.append(get_memory_usage())
    avg = sum(memory_usages) / len(memory_usages)
    print(f'Average memory usage: {avg:.1f} MB')

if __name__ == '__main__':
    print_memory_usage('Initial memory usage')
    write_at_once(TEN_GB)
    print_memory_usage('10GB has been written to disk at once')
    write_pieces(TEN_GB, 100 * 1024 ** 2)
    print_memory_usage('10GB has been written to disk in pieces')
