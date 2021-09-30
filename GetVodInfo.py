import requests


class GetVodInfo:
    headers = {'Client-ID': '37v97169hnj8kaoq8fs3hzz8v6jezdj', 
    'Accept': 'application/vnd.twitchtv.v5+json'}
    api_path = "https://api.twitch.tv/kraken/videos/{}"

    def __init__(self):
        self._video_id = None
        self.info_json = None
        self.data = None

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, value:str):
        self._video_id = value

    def get_json(self):
        failed = False
        if self.video_id:
            api_path = self.api_path.format(self.video_id)
            try:
                response = requests.get(api_path, headers=self.headers)
            except Exception as e:
                failed = True
                return failed

            if response.status_code == 200:
                self.info_json = response.json()

        return failed

    def get_data(self):
        if self.info_json:
            self.data = {}
            self.data['id'] = self.info_json['channel']['name']
            self.data['name'] = self.info_json['channel']['display_name']
            self.data['title'] = self.info_json['title']
            self.data['length'] = self.info_json['length']
            self.data['game'] = self.info_json['game']
            self.data['fps'] = self.info_json['fps']
            self.data['resolutions'] = self.info_json['resolutions']

            if self.info_json['published_at']:
                self.data['start_time'] = self.info_json['published_at']
            else:
                self.data['start_time'] = self.info_json['created_at']

            self.data['preview_image_path'] = self.info_json['preview']['medium']
    