# from extensions import cache
from datetime import datetime

def log_cache_access(cache_key, hit):
    with open("cache_log.txt", "a") as f:
        status = "hit" if hit else "miss"
        f.write(f"Cache {status}: {cache_key} at {datetime.now()}\n")