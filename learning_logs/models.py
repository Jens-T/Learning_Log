from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'


    def __str__(self):
        return f"{self.text[:50]}..." 
    
class Comment(models.Model):
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    date_added = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"
    
class TopicMember(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    permission = models.CharField(
        max_length=10,
        choices=[
            ('view', 'View only'),
            ('edit', 'Can edit'),
        ],
        default='view'
    )

    def __str__(self):
        return f"{self.user.username} - {self.topic.text}"
    
class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    message = models.CharField(max_length=255)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )
