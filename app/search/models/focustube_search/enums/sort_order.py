from enum import Enum


class SortOrder(str, Enum):
    relevance = 'relevance'
    uploadDate = 'uploadDate'
    viewCount = 'viewCount'
    rating = 'rating'
