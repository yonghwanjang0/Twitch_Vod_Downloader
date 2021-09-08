import shutil
import os


class FilesMerger:
    def __init__(self):
        self._temp_folder_path = None
        self._target_folder_path = None

    # temp files save folder path
    @property
    def temp_folder_path(self):
        return self._temp_folder_path

    @temp_folder_path.setter
    def temp_folder_path(self, folder_path):
        self._temp_folder_path = folder_path

    # target folder path (the merged finish file save folder)
    @property
    def target_folder_path(self):
        return self._target_folder_path

    @target_folder_path.setter
    def target_folder_path(self, folder_path):
        self._target_folder_path = folder_path

    def merge_files(self, index_range, filename):
        start_number, last_number = (
            index_range[0], index_range[1] + 1)
        target_file = self.target_folder_path + filename

        with open(target_file, 'wb') as merged:
            for index in range(start_number, last_number):
                current_stream_file = (
                    "".join([self.temp_folder_path, str(index).zfill(8), ".ts"]))
                with open(current_stream_file, 'rb') as merge_file:
                    shutil.copyfileobj(merge_file, merged)
                os.remove(current_stream_file)
            os.rmdir(self.temp_folder_path)
