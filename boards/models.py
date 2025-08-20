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
    def last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
