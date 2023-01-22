from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    read = models.BooleanField(default=False)
    unsent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @property
    def last_messages(self):
        return Message.objects.order_by('-timestamp')[:10

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
