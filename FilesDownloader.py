import requests
import shutil
import os
import asyncio


class FilesDownloader:
    def __init__(self):
        self._playlist = None
        self._save_folder_path = None

    # playlist object
    @property
    def playlist(self):
        return self._playlist

    @playlist.setter
    def playlist(self, value:object):
        self._playlist = value

    # temp files save folder path
    @property
    def save_folder_path(self):
        return self._save_folder_path

    @save_folder_path.setter
    def save_folder_path(self, folder_path:str):
        self._save_folder_path = folder_path

    @staticmethod
    def get_requests(url, timeout=5):
        try:
            current_file = requests.get(url, stream=True, timeout=timeout)
        except Exception as e:
            current_file = requests.get(url, stream=True, timeout=timeout)

        return current_file

    @staticmethod
    def write_file(current_file, save_path):
        with open(save_path, 'wb') as f:
            current_file.raw.decode_content = True
            shutil.copyfileobj(current_file.raw, f)

    async def download_single_file(self, index):
        return_value = [False, index, ""]
        try_count = 0
        url = self.playlist.segments[index].absolute_uri
        save_path = self.save_folder_path + str(index).zfill(8) + ".ts"

        current_file = self.get_requests(url)
        while try_count < 3:
            if current_file.status_code == 200:
                self.write_file(current_file, save_path)

                measured_size = os.path.getsize(save_path)
                origin_size = int(current_file.headers["Content-Length"])
                if origin_size == measured_size:
                    return_value = [True, index, ""]
                    break

            else:
                try_count += 1
                return_value[2] = url
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
