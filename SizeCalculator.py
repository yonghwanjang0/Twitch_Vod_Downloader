import requests


class SizeCalculator:
    def __init__(self):
        self._playlist = None
        self.single_file_size = None

    @property
    def playlist(self):
        return self._playlist

    @playlist.setter
    def playlist(self, value:object):
        self._playlist = value

    def get_single_file_size(self):
        size = None
        for segment in self.playlist.segments:
            if "muted" not in segment.uri:
                file = requests.get(segment.absolute_uri, stream=True)
                size = int(file.headers["Content-Length"])
                break
        
        if size:
            self.single_file_size = size

    def get_total_size(self):
        length = len(self.playlist.segments)
        total_size = self.single_file_size * length

        return total_size
    
    @staticmethod
    def convert_size_units(size:int):
        giga = (1024 ** 3)
        mega = (1024 ** 2)
        if int(size / giga) >= 1:
            convert = round((size / giga), 2)
            result = (convert, "GB")
        else:
            convert = round((size / mega), 2)
            result = (convert, "MB")
        
        return result

    def run(self, playlist_object):
        self.playlist = playlist_object
        self.get_single_file_size()
        total_size = self.get_total_size()

        return total_size
