from django.db import models


class Discussion(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
