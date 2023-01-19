from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_message', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        self.author.username

    def last_messages(self):
        return Message.objects.order_by('-timestamp')[:10]