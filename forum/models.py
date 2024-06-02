from django.db import models
from django.conf import settings


class Discussion(models.Model):
    """
    Represents a forum discussion.

    Attributes:
        title (str): The title of the discussion.
        author (User, optional): The user who created the discussion. This field can be null if the discussion was created
                                 without an associated user, for example, by an automated process or before user implementation.
        created_at (datetime): The date and time the discussion was created, automatically set when the discussion is first saved.

    Fields:
        title (models.CharField): Stores the title of the discussion, with a maximum length of 200 characters.
        author (models.ForeignKey): Links to the Django user model. It is nullable to allow discussions without an explicit author.
                                    Uses 'settings.AUTH_USER_MODEL' to support custom user models.
        created_at (models.DateTimeField): Automatically records the time the discussion was created, not modifiable.
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discussions",
        null=True,
    )
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


class Notification(models.Model):
    """
    Represents a notification related to user activities within the forum.

    Attributes:
        user (ForeignKey): The user who will receive the notification.
        message (TextField): The content of the notification message.
        read (BooleanField): Status to indicate if the notification has been read.
        created_at (DateTimeField): The date and time the notification was created, automatically set to now when the object is created.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the notification, showing the user and read status."""
        return f'Notification for {self.user.username} - {"Read" if self.read else "Unread"}'
