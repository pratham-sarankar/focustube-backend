from enum import Enum


class SearchType(str, Enum):
    videos = 'videos'
    channels = 'channels'
    playlists = 'playlists'
    films = 'films'
