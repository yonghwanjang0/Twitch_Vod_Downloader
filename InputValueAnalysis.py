from GetPlaylist import GetPlaylist


class InputValueAnalysis:
    def __init__(self):
        self._input_value = None
        self.input_value_type = None
        self.vod_id = None

        self.playlist_getter = GetPlaylist()

    @property
    def input_value(self):
        return self._input_value

    @input_value.setter
    def input_value(self, value):
        self._input_value = value

    def set_value_type(self):
        if self.input_value.isdecimal():
            self.input_value_type = "Vod_ID"
        elif "twitch.tv/videos/" in self.input_value:
            if "?filter=" in self.input_value:
                self.input_value_type = "Vod_Path_With_Option"
            else:
                self.input_value_type = "Vod_Path"
        else:
            self.input_value_type = "Do_not_Valid_String"

    def get_video_id(self):
        value_args = self.input_value.split("/")
        id_value = value_args[-1].split("?")[0]

        is_integer = id_value.isdecimal()
        if is_integer:
            self.vod_id = id_value
        else:
            self.input_value_type = "Do_not_Valid_String"

    def check_exists(self):
        self.playlist_getter.check_remove_video()

    def get_id_info(self):
        self.playlist_getter.get_token()
        self.playlist_getter.check_subscribers_only()

    def get_playlist_path(self):
        self.playlist_getter.get_playlist()

    def run(self, input_value:str):
        self.playlist_getter.__init__()
        self.input_value = input_value
        self.set_value_type()
        if self.input_value_type != "Do_not_Valid_String":
            self.get_video_id()
        else:
            return ["not valid"]

        if self.vod_id is not None:
            self.playlist_getter.set_video_id(self.vod_id)
            self.playlist_getter.get_data_json()
            self.check_exists()
        else:
            return ["not valid"]

        if not self.playlist_getter.delete_vod:
            self.get_id_info()
        else:
            return ["not exists"]

        if not self.playlist_getter.subscribers_only:
            self.get_playlist_path()
            infomation_list = []
            if self.playlist_getter.playlist_path:
                infomation_list.append(self.vod_id)
                infomation_list.append(self.playlist_getter.playlist_path)
            return infomation_list
        else:
            return ["subscribers only"]
