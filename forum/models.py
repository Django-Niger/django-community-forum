from django.db import models


class Discussion(models.Model):
    """
    Represents a forum discussion.

    Attributes:
        title (str): The title of the discussion.
        created_at (datetime): The date and time the discussion was created.
    """

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    """
    Represents a post within a discussion.

    Attributes:
        discussion (Discussion): The discussion to which the post belongs.
        author (User): The user who authored the post.
        content (str): The content of the post.
        created_at (datetime): The date and time the post was created.
    """

    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
