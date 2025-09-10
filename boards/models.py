from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    @property
    def posts_count(self):
        return sum(topic.posts.count() for topic in self.topics.all())

    @property
    def last_post_date(self):
        last_post = Post.objects.filter(
            topic__board=self
        ).order_by('-created_at').first()
        return last_post.created_at if last_post else None

class Topic(models.Model):
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Post(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.created_by.username} on {self.topic.title}"
