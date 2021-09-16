import requests
import time


class GetPlaylist:
    headers = {'Client-ID': "kimne78kx3ncx6brgo4mv6wki5h1ko"}

    def __init__(self):
        self.data = None
        self.token = None
        self.sig = None
        self.video_id = None
        self.playlist_path = None
        self.subscribers_only = None

    def set_video_id(self, video_id:str):
        # input type of video_id : string
        self.video_id = video_id
        self.data = ('{"operationName":"PlaybackAccessToken_Template",'
                     '"query":"query PlaybackAccessToken_Template($login: '
                     'String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, '
                     '$playerType: String!) {  streamPlaybackAccessToken'
                     '(channelName: $login, params: {platform: \\"web\\", '
                     'playerBackend: \\"mediaplayer\\", playerType: '
                     '$playerType}) @include(if: $isLive) {    value    '
                     'signature    __typename  }  videoPlaybackAccessToken'
                     '(id: $vodID, params: {platform: \\"web\\", '
                     'playerBackend: \\"mediaplayer\\", playerType: '
                     '$playerType}) @include(if: $isVod) {    value    signature'
                     '    __typename  }}","variables":{"isLive":false,"login":"",'
                     '"isVod":true,"vodID":"' + video_id + '","playerType":"embed"}}')

    def get_token(self):
        path = "https://gql.twitch.tv/gql"
        result = self.get_loop(path, "Token")
        result_parse = result.json()["data"]["videoPlaybackAccessToken"]

        self.token = result_parse["value"]
        self.sig = result_parse["signature"]

    def get_playlist(self):
        path = ("http://usher.twitch.tv/vod/{0}?nauth={1}&nauthsig={2}"
                "&allow_source=true&player=twitchweb"
                .format(self.video_id, self.token, self.sig))
        result = self.get_loop(path, "Playlist")

        playlist_expected = result.text.split("\n")
        for text in playlist_expected:
            if "chunked" in text and "m3u8" in text:
                self.playlist_path = text
                break

    def get_loop(self, path, position):
        count = 0
        while count < 3:
            try:
                if position == "Token":
                    t = requests.post(path, data=self.data, headers=self.headers)
                else:
                    t = requests.get(path, headers=self.headers)
                return t
            except Exception as e:
                count += 1
                time.sleep(5)

    def check_subscribers_only(self):
        front_string = '''{"restricted_bitrates":'''
        back_string = '''},"device_id"'''
        front_index = self.token.find(front_string) + len(front_string)
        back_index = self.token.find(back_string)
        restricted = self.token[front_index:back_index]
        if "[]" in restricted:
            self.subscribers_only = False
        else:
            self.subscribers_only = True
