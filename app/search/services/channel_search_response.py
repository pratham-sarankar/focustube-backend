from youtubesearchpython import Channel, ChannelRequestType


class ChannelSearchService:
    def __init__(self, id):
        self.id = id
        pass

    def get_info(self):
        info_search: Channel = Channel(channel_id=self.id, request_type=ChannelRequestType.info)
        return info_search.result

    def get_playlists(self):
        playlist_search: Channel = Channel(channel_id=self.id, request_type=ChannelRequestType.playlists)
        playlists = playlist_search.result['playlists']
        for playlist in playlists:
            playlist['channel'] = {
                'name': playlist_search.result['title'],
                'id': playlist_search.result['id'],
                'link': playlist_search.result['url'],
                'thumbnails': playlist_search.result['thumbnails']
            }
        return playlists
