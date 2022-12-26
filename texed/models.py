
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Chat(models.Model):
    user_1      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1')
    user_2      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2')

    def __int__(self):
        return self.id

class Message(models.Model):

    sender      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    chat_id     = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat")
    message     = models.TextField(max_length=5000)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.id
