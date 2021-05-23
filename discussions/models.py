from django.shortcuts import reverse
from django.db import models
from . import managers

#기업토론
class Discussion(models.Model):

    #참여자
    participants = models.ManyToManyField(
        "users.User", related_name="discussions", blank=True
    )

    #기업
    corp = models.ForeignKey(
        "corps.Corp", related_name="discussions", on_delete=models.CASCADE
    )

    #주제
    topic = models.CharField(max_length=300)

    objects = managers.CustomModelManager()

    def __str__(self):
        return self.topic + " - " + self.corp.corp_name

    def count_messages(self):
        return self.messages.count()

    def count_participants(self):
        return self.participants.count()

    count_messages.short_description = "Number of Messages"


class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    discussion = models.ForeignKey(
        "Discussion", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"