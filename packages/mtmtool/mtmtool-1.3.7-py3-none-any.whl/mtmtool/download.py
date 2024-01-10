import os
import hashlib
import threading
import time
from queue import Queue
from urllib.parse import unquote, urlparse

import requests

from mtmtool.log import stream_logger


QUENE_DEQUENE_DELAY = 0.1
TRUST_HOSTNAMES_IN_REDIRECTING = ["urs.earthdata.nasa.gov"]
GLOBAL_DOWNLOAD_LOCK = threading.Lock()

logger = stream_logger("Down")
logger_io = stream_logger("IO")


def extract_filename_from_headers(headers):
    # 检查 Content-Disposition header 是否存在
    if "Content-Disposition" in headers:
        # 从 Content-Disposition header 中提取文件名
        content_disposition = headers["Content-Disposition"]
        _, params = content_disposition.split(";")
        filename_param = next(
            (param.strip() for param in params.split(";") if param.strip().startswith("filename=")), None
        )

        if filename_param:
            _, filename = filename_param.split("=")
            filename = unquote(filename.strip('"'))
            return filename
    else:
        return ""


class TrustHostnameSession(requests.Session):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.trust_hostnames = kwargs.get("trust_hostnames", TRUST_HOSTNAMES_IN_REDIRECTING)

    def should_strip_auth(self, old_url, new_url):
        raw_flag = super().should_strip_auth(old_url, new_url)
        if raw_flag and urlparse(new_url).hostname in self.trust_hostnames:
            return False
        return raw_flag


class FileIntegrity:
    @staticmethod
    def size(path):
        if not os.path.isfile(path):
            return -1
        return os.path.getsize(path)

    @staticmethod
    def md5(path):
        if not os.path.isfile(path):
            return ""
        with open(path, "rb") as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            return md5.hexdigest()

    @staticmethod
    def rm(path):
        if not os.path.exists(path):
            return
        try:
            os.remove(path)
            info_text = "File remove success!"
        except Exception:
            info_text = "File remove failed!"
        logger_io.info(f"{info_text} {path}")


class SingleConnectionDownloaderThread(threading.Thread):
    def __init__(
        self,
        queue: Queue,
        session=None,
        timeout=None,
        check_integrity=False,
        should_wait=False,
        only_file=True,
        **kwargs,
    ):
        super().__init__(daemon=kwargs.get("daemon", None))  # 线程守护

        # 设置请求会话
        self.session = session or TrustHostnameSession()  # requests session
        if "cookies" in kwargs:
            self.session.cookies.update(kwargs["cookies"])
        if "headers" in kwargs:
            self.session.headers.update(kwargs["headers"])
        if "auth" in kwargs:
            self.session.auth = kwargs["auth"]
        if "proxies" in kwargs:
            self.session.proxies = kwargs["proxies"]
        if "trust_hostnames" in kwargs:
            self.session.trust_hostnames = kwargs["trust_hostnames"]

        # 设置下载任务队列
        self.quene = queue if queue else None  # 下载任务队列
        self.should_wait = should_wait  # 是否等待下载任务, 每次下载任务完成后, 等待wait_event被唤醒
        self.only_file = only_file

        assert isinstance(queue, Queue), "queue is not Queue class"

        # 下载任务默认参数
        self.default = {
            "method": "GET",
            "url": "https://",
            "filedir": "",
            "filename": "",
            "size": -1,
            "md5": "",
            "chunk_size": 1024 * 1024,
            "timeout": timeout,
            "check_integrity": check_integrity,
        }

        # 线程控制条件
        self.wait_event = threading.Event()
        self.running = False
        self.error = None
        self.exit = False

    def check_file_integrity(self, item, force=False):
        # 检查文件md5
        if md5 := FileIntegrity.md5(item.get("path", "")) if item.get("md5", "") else None:
            return md5 == (item.get("md5", ""))
        # 检查文件大小
        if size := FileIntegrity.size(item.get("path", "")) if item.get("size", -1) > 0 else None:
            return size == (item.get("size", -1))
        # 看看是否设置了不检查文件完整性, 如果设置中不检查文件完整性, 则默认为完整
        if not item.get("check_integrity", False) and not force:  # force参数用于强制检查文件完整性
            return True
        return False

    def get_file_path(self, item, headers):
        # 获取文件路径
        web_file_name = extract_filename_from_headers(headers)
        url_file_name = os.path.basename(urlparse(item.get("url", "")).path)
        raw_file_name = os.path.basename(item.get("filename", "")) if item.get("filename", "") else ""
        if raw_file_name:
            file_name = raw_file_name
        elif web_file_name:
            file_name = web_file_name
        elif url_file_name:
            file_name = url_file_name
        file_dir = item.get("filedir", "")
        if file_dir:
            file_path = os.path.join(file_dir, file_name)
        else:
            file_path = file_name
        assert file_name, f"File name {file_name} is empty"
        return file_path, file_dir, file_name

    def print_success_info(self, item):
        filesize = FileIntegrity.size(item["path"])
        info_text = "File Downloaded ({:.4f}MB)!".format(filesize / 1024 / 1024)
        file_name = os.path.basename(item["path"])
        logger.info(f"{info_text} {file_name}")

    def run(self):
        while True:
            # 等待线程被唤醒
            self.wait_event.wait() if self.should_wait else None

            # 检查是否退出
            if self.exit:
                break

            # 获取下载任务
            item = self.default.copy()
            item.update(self.quene.get())
            self.running = True
            response = None

            try:
                # 发送请求
                response = self.session.request(
                    method="HEAD",
                    url=item.get("url", "https://"),
                    timeout=item.get("timeout", None),
                    stream=False,
                    allow_redirects=True,
                )
                response.raise_for_status()
                response.close()
                headers = response.headers.copy()

                # 检查请求是否是文件下载请求
                if self.only_file and "Content-Length" not in headers and headers["Content-Type"].startswith("text"):
                    logger.error(f"{item.get('url', 'https://')} is not a file!")
                    continue

                # 获取文件路径
                file_path, file_dir, file_name = self.get_file_path(item, headers)
                item["path"] = file_path

                # 获取文件大小
                response_content_length = int(headers.get("Content-Length", -1))
                if item.get("size", -1) < 0 and response_content_length > 0:
                    item["size"] = response_content_length

                # 记录此次请求的信息
                GLOBAL_DOWNLOAD_LOCK.acquire()  # 申请全局锁
                with open(".downtmp", "a") as fp:
                    text = item.get("url", "https://") + "," + file_name + "," + str(response_content_length) + "\n"
                    fp.write(text)
                GLOBAL_DOWNLOAD_LOCK.release()  # 释放全局锁

                # 下载前强制检查文件完整性, 如果文件不完整, 则删除文件重新下载, 如果文件完整, 则跳过下载
                is_integrity_predownload = self.check_file_integrity(item, force=True)
                if is_integrity_predownload:
                    self.print_success_info(item)
                    continue

                # 删除之前的文件
                FileIntegrity.rm(file_path)

                # 分块下载文件
                logger.info(f"Downloading File: {file_name}")
                response = self.session.request(
                    method=item.get("method", "GET"),
                    url=item.get("url", "https://"),
                    timeout=item.get("timeout", None),
                    stream=True,
                    allow_redirects=True,
                )
                response.raise_for_status()
                with open(file_path, "wb") as fd:
                    for chunk in response.iter_content(chunk_size=item.get("chunk_size", None)):
                        fd.write(chunk)

                # 检查文件完整性, 如果要求检查文件且文件不完整, 则删除文件
                is_integrity = self.check_file_integrity(item, force=False)
                if is_integrity:
                    self.print_success_info(item)
                else:
                    FileIntegrity.rm(file_path)

            except requests.exceptions.RequestException as e:
                logger.error(e)
            except Exception as e:
                self.error = e
            finally:
                # 单次任务完成
                response.close() if response else None
                self.running = False
                self.wait_event.clear() if self.should_wait else None


class SingleConnectionDownloaderThreadPool:
    quene_default = Queue()

    def __init__(self, max_threads=1, **kwargs) -> None:
        super().__init__()
        self.max_threads = max_threads
        self.quene = Queue()
        kwargs.update(
            {
                "queue": self.quene,
                "daemon": True,
                "should_wait": True,
            }
        )
        self.kwargs = kwargs
        pass

    def put(self, **kwargs):
        self.quene.put(kwargs)

    def start(self):
        self.downloader_pools = [SingleConnectionDownloaderThread(**self.kwargs) for _ in range(self.max_threads)]
        for thread in self.downloader_pools:
            thread.wait_event.clear()
            thread.start()
        while True:
            for thread in self.downloader_pools:
                if thread.error:
                    raise thread.error
            if self.quene.empty():
                if not any([thread.running for thread in self.downloader_pools]):
                    for thread in self.downloader_pools:
                        thread.exit = True
                        thread.wait_event.set()
                    break
                time.sleep(0.1)
            else:
                for thread in self.downloader_pools:
                    if not thread.wait_event.is_set():
                        thread.wait_event.set()
                        break
                time.sleep(QUENE_DEQUENE_DELAY)


def download_from_dataframe(
    pool: SingleConnectionDownloaderThreadPool,
    df,
    tmp_csv: str = "tempfileinfos.csv",
    loop: int = 10,
):
    import pandas as pd

    # 检查输入参数
    df = df.copy()
    if df.empty:
        logger.error("下载任务为空!")
        return
    if "url" not in df.columns:
        logger.error("'url' column is not in the pandas.dataframe!")
        return
    if loop < 1:
        logger.error("param 'loop' must be greater than 0!")
        return
    if "complete" not in df.columns:  # 如果没有下载完成标志位, 则添加下载完成标志位
        df["complete"] = False

    # 变量初始化
    flag_all_complete = False  # 是否所有文件都下载完成, 如果所有文件都下载完成, 则跳过下载, 否则继续下载
    actual_total_count = 0  # 计数器, 用于记录下载次数
    for _ in range(loop):
        # 变量初始化
        _count = 0  # 计数器, 用于记录迭代下载次数

        # 检查是否有文件名称字段, 如果没有, 则设置为空
        if "filename" not in df.columns:
            df["filename"] = ""

        # 将未完成下载的文件加入下载队列
        for _, row in df.iterrows():
            # 变量初始化
            _dict = {}
            filepath = None
            is_complete = row["complete"]  # 获取下载完成标志位
            # 获取下载的文件路径
            if "filedir" in row and row["filedir"]:  # 如果有文件夹字段, 则使用文件夹字段
                _dict["filedir"] = row["filedir"]
            if "filename" in row and row["filename"]:  # 如果有文件名字段, 则使用文件名字段
                _dict["filename"] = row["filename"]
            if "filename" in _dict:  # 如果有文件夹和文件名字段, 则跳过
                if "filedir" in _dict:
                    filepath = os.path.join(_dict["filedir"], _dict["filename"])  # 拼接文件路径
                else:
                    filepath = _dict["filename"]
            # 检查文件路径是否需要下载
            if not is_complete:
                if filepath is not None and os.path.isfile(filepath):  # 如果文件已经存在
                    # 获取文件完整性信息
                    flag_file_size = "size" in row and row["size"] > 0 and FileIntegrity.size(filepath) == row["size"]
                    flag_file_md5 = "md5" in row and row["md5"] and FileIntegrity.md5(filepath) == row["md5"]
                    if "md5" in row:
                        if flag_file_md5:
                            is_complete = True
                    else:
                        if flag_file_size:
                            is_complete = True
                # 如果文件没有完全下载, 则加入下载队列
                if not is_complete:
                    _dict.update(row.to_dict())  # 将行数据转换为字典, 更新到下载字典中
                    pool.put(**_dict)  # 将下载字典加入下载队列
                    actual_total_count += 1  # 计数器加1
                    _count += 1  # 计数器加1
            row["complete"] = is_complete  # 更新下载完成标志位

        # 开始下载
        pool.start()

        # 后处理
        if os.path.exists(".downtmp") and tmp_csv is not None:
            df_temp = pd.read_csv(".downtmp", header=None, names=["url", "filename", "size"])
            # 剔除文件大小小于0的文件, 按文件大小升序排序, 去除重复文件, 保留最后一个文件
            df_temp.drop(index=df_temp[df_temp["size"] < 0].index, inplace=True)
            df_temp.sort_values(by=["size"], ascending=[True], inplace=True)
            df_temp.drop_duplicates(subset=["url"], keep="last", inplace=True)
            df_merge = df.merge(df_temp, on="url", how="left", suffixes=("", "_y"))
            # 当出现重复字段时, 使用新字段的值替换原始字段的值
            if "filename_y" in df_merge.columns:
                df["filename"] = df_merge["filename_y"].fillna(df_merge["filename"])
            if "size_y" in df_merge.columns:
                df["size"] = df_merge["size_y"].fillna(df_merge["size"])
            # 删除全为nan值的列
            df.dropna(axis=1, how="all", inplace=True)
            # 保存文件
            df.to_csv(tmp_csv, index=False)
            # 删除临时文件
            FileIntegrity.rm(".downtmp")

        if _count == 0:  # 如果本次迭代没有下载任务, 则说明全部下载成功, 退出循环
            flag_all_complete = True
            break

    text = "下载完成" if flag_all_complete else "下载未完成"
    logger.info(f"{text}, 本次共尝试下载{actual_total_count}次")

    if tmp_csv is not None:
        logger.info(f"本次下载的文件完整信息请查看: {tmp_csv}")
