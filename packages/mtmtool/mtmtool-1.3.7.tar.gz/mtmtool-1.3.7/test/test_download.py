import mtmtool.download as dd
import time


pool = dd.SingleConnectionDownloaderThreadPool(max_threads=2, only_file=False)
pool.put(url="https://www.baidu.com", filename="baidu0.html")
pool.put(url="https://www.baidu.com", filename="baidu1.html")

pool.start()
