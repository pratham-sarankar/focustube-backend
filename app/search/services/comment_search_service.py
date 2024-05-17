from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
from itertools import islice


class CommentSearchService:
    def __init__(self, id: str):
        self.id = id

    def search(self):
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments(self.id, sort_by=SORT_BY_RECENT)
        result = []
        for comment in islice(comments, 20):
            result.append(comment)
        return result
