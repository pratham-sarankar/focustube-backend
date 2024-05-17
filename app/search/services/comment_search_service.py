from youtubesearchpython import Comments


class CommentSearchService:
    def __init__(self, id: str):
        self.id = id

    def search(self):
        comments = Comments("https://www.youtube.com/watch?v=2V7yPrxJ8Ck")
        while comments.hasMoreComments:
            print("Fetching more comments")
            comments.getNextComments()
            print(comments.comments["result"])
        return comments.comments["result"]
