from django.db import models
from django.conf import settings


# Create your models here.
class MessageThread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='message_threads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Thread with {", ".join(user.username for user in self.participants.all())}'


class Message(models.Model):
    thread = models.ForeignKey(MessageThread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} in thread {self.thread.id}'
