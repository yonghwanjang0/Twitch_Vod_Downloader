import requests
import shutil
import os
import asyncio


class FileDownloader:
    def __init__(self):
        self._address_root = None
        self._save_folder_path = None

    # root part at vod files url
    @property
    def address_root(self):
        return self._address_root

    @address_root.setter
    def address_root(self, value):
        self._address_root = value

    # temp files save folder path
    @property
    def save_folder_path(self):
        return self._save_folder_path

    @save_folder_path.setter
    def save_folder_path(self, folder_path):
        self._save_folder_path = folder_path

    @staticmethod
    def get_requests(url, timeout=5):
        current_file = requests.get(url, stream=True, timeout=timeout)

        return current_file

    @staticmethod
    def write_file(current_file, save_path):
        with open(save_path, 'wb') as f:
            current_file.raw.decode_content = True
            shutil.copyfileobj(current_file.raw, f)

    async def download_single_file(self, index):
        return_value = [False, index]
        try_count = 0
        url = self.address_root + str(index) + ".ts"
        save_path = self.save_folder_path + str(index).zfill(8) + ".ts"

        current_file = self.get_requests(url)
        while try_count < 3:
            if current_file.status_code == 200:
                self.write_file(current_file, save_path)

                measured_size = os.path.getsize(save_path)
                origin_size = int(current_file.headers["Content-Length"])
                if origin_size == measured_size:
                    return_value = [True, index]
                    break

            else:
                try_count += 1
                current_file = self.get_requests(url)

        return return_value

    async def bundle_of_downloads(self, index_list):
        task_list = []
        for index in index_list:
            if index:
                task = asyncio.ensure_future(
                    self.download_single_file(index))
                task_list.append(task)
        result = await asyncio.gather(*task_list)

        return result
