import os
import mtmtool.download as dd
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pool = dd.SingleConnectionDownloaderThreadPool(max_threads=2, only_file=False)
df = pd.read_csv("test_download_csv.csv")
dd.download_from_dataframe(pool, df)
