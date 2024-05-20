from app.search.models.focustube_search.enums import SearchType, UploadDateFilter, SortOrder
from youtubesearchpython import VideoDurationFilter

class SearchPreference:
    def __init__(self, search_type: SearchType | None, upload_date_filter: UploadDateFilter | None,
                 sort_order: SortOrder = SortOrder.relevance):
        self.search_type = search_type
        self.upload_date_filter = upload_date_filter
        self.sort_order = sort_order

    def validate(self):
        if self.search_type is not SearchType.videos and self.search_type is not SearchType.films:
            if self.upload_date_filter is not None:
                raise ValueError("Sort order is not applicable for this search type")
        elif SearchPreference.decode_search_preference(self) is None:
            raise ValueError("Invalid search preference")

    def get_code(self):
        self.validate()
        code = SearchPreference.decode_search_preference(self)
        return code

    def __eq__(self, other):
        return (self.search_type == other.search_type and self.upload_date_filter == other.upload_date_filter
                and self.sort_order == other.sort_order)

    def __hash__(self):
        return hash((self.search_type, self.upload_date_filter, self.sort_order))

    @staticmethod
    def decode_search_preference(sp: 'SearchPreference') -> str | None:
        search_preferences = {
            # No filter selected
            SearchPreference(None, None, SortOrder.relevance): None,

            # Search Type : videos, Date Filter : None, and every possible sort order
            SearchPreference(SearchType.videos, None, SortOrder.relevance): "EgIQAQ%3D%3D",
            SearchPreference(SearchType.videos, None, SortOrder.uploadDate): "CAISAhAB",
            SearchPreference(SearchType.videos, None, SortOrder.viewCount): "CAMSAhAB",
            SearchPreference(SearchType.videos, None, SortOrder.rating): "CAESAhAB",

            # Search Type : videos, Date Filter : Last hour, and every possible sort order
            SearchPreference(SearchType.videos, UploadDateFilter.lastHour, SortOrder.relevance): "CAASBAgBEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.lastHour, SortOrder.uploadDate): "CAISBAgBEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.lastHour, SortOrder.viewCount): "CAMSBAgBEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.lastHour, SortOrder.rating): "CAESBAgBEAE%3D",

            # Search Type : videos, Date Filter : Today, and every possible sort order
            SearchPreference(SearchType.videos, UploadDateFilter.today, SortOrder.relevance): "CAASBAgCEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.today, SortOrder.uploadDate): "CAISBAgCEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.today, SortOrder.viewCount): "CAMSBAgCEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.today, SortOrder.rating): "CAESBAgCEAE%3D",

            # Search Type : videos, Date Filter : This week, and every possible sort order
            SearchPreference(SearchType.videos, UploadDateFilter.thisWeek, SortOrder.relevance): "CAASBAgDEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisWeek, SortOrder.uploadDate): "CAISBAgDEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisWeek, SortOrder.viewCount): "CAMSBAgDEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisWeek, SortOrder.rating): "CAESBAgDEAE%3D",

            # Search Type : videos, Date Filter : This month, and every possible sort order
            SearchPreference(SearchType.videos, UploadDateFilter.thisMonth, SortOrder.relevance): "CAASBAgEEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisMonth, SortOrder.uploadDate): "CAISBAgEEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisMonth, SortOrder.viewCount): "CAMSBAgEEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisMonth, SortOrder.rating): "CAESBAgEEAE%3D",

            # Search Type : videos, Date Filter : This year, and every possible sort order
            SearchPreference(SearchType.videos, UploadDateFilter.thisYear, SortOrder.relevance): "CAASBAgFEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisYear, SortOrder.uploadDate): "CAISBAgFEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisYear, SortOrder.viewCount): "CAMSBAgFEAE%3D",
            SearchPreference(SearchType.videos, UploadDateFilter.thisYear, SortOrder.rating): "CAESBAgFEAE%3D",

            # Search Type : channels, and every possible sort order
            SearchPreference(SearchType.channels, None, SortOrder.relevance): "CAASAhAC",
            SearchPreference(SearchType.channels, None, SortOrder.uploadDate): "CAISAhAC",
            SearchPreference(SearchType.channels, None, SortOrder.viewCount): "CAMSAhAC",
            SearchPreference(SearchType.channels, None, SortOrder.rating): "CAESAhAC",

            # Search Type : playlists, and every possible sort order
            SearchPreference(SearchType.playlists, None, SortOrder.relevance): "CAASAhAD",
            SearchPreference(SearchType.playlists, None, SortOrder.uploadDate): "CAISAhAD",
            SearchPreference(SearchType.playlists, None, SortOrder.viewCount): "CAMSAhAD",
            SearchPreference(SearchType.playlists, None, SortOrder.rating): "CAESAhAD",

            # Search Type : films, and every possible sort order
            SearchPreference(SearchType.films, None, SortOrder.relevance): "CAASAhAE",
            SearchPreference(SearchType.films, None, SortOrder.uploadDate): "CAISAhAE",
            SearchPreference(SearchType.films, None, SortOrder.viewCount): "CAMSAhAE",
            SearchPreference(SearchType.films, None, SortOrder.rating): "CAESAhAE",

            # Search Type : films, Date Filter : Last hour, and every possible sort order
            SearchPreference(SearchType.films, UploadDateFilter.lastHour, SortOrder.relevance): "CAASBAgBEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.lastHour, SortOrder.uploadDate): "CAISBAgBEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.lastHour, SortOrder.viewCount): "CAMSBAgBEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.lastHour, SortOrder.rating): "CAESBAgBEAQ%3D",

            # Search Type : films, Date Filter : Today, and every possible sort order
            SearchPreference(SearchType.films, UploadDateFilter.today, SortOrder.relevance): "CAASBAgCEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.today, SortOrder.uploadDate): "CAISBAgCEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.today, SortOrder.viewCount): "CAMSBAgCEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.today, SortOrder.rating): "CAESBAgCEAQ%3D",

            # Search Type : films, Date Filter : This week, and every possible sort order
            SearchPreference(SearchType.films, UploadDateFilter.thisWeek, SortOrder.relevance): "CAASBAgDEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisWeek, SortOrder.uploadDate): "CAISBAgDEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisWeek, SortOrder.viewCount): "CAMSBAgDEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisWeek, SortOrder.rating): "CAESBAgDEAQ%3D",

            # Search Type : films, Date Filter : This month, and every possible sort order
            SearchPreference(SearchType.films, UploadDateFilter.thisMonth, SortOrder.relevance): "CAASBAgEEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisMonth, SortOrder.uploadDate): "CAISBAgEEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisMonth, SortOrder.viewCount): "CAMSBAgEEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisMonth, SortOrder.rating): "CAESBAgEEAQ%3D",

            # Search Type : films, Date Filter : This year, and every possible sort order
            SearchPreference(SearchType.films, UploadDateFilter.thisYear, SortOrder.relevance): "CAASBAgFEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisYear, SortOrder.uploadDate): "CAISBAgFEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisYear, SortOrder.viewCount): "CAMSBAgFEAQ%3D",
            SearchPreference(SearchType.films, UploadDateFilter.thisYear, SortOrder.rating): "CAESBAgFEAQ%3D",

            # Search Type : shorts, Date Filter : None, and every possible sort order
            SearchPreference(SearchType.shorts, None, SortOrder.relevance): f"{VideoDurationFilter.short}",
        }
        return search_preferences.get(sp)
