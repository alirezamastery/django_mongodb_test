import uuid

from django.db import models
from django.utils import timezone


class ChatMessage(models.Model):
    class StateChoices(models.IntegerChoices):
        SAVED = 1
        SENT = 2
        SEEN = 3

    user = models.BigIntegerField(blank=False)
    recipient = models.BigIntegerField(blank=False)
    body = models.TextField('body', blank=True, null=True)
    document = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, blank=True, null=True)
    edited = models.BooleanField(default=False)
    file_type = models.SmallIntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True, verbose_name='اطلاعات اضافی پیام')
    state = models.SmallIntegerField(choices=StateChoices.choices, default=StateChoices.SAVED)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now_add=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    client_key = models.UUIDField(blank=False, null=False, unique=True, default=uuid.uuid4)

    def __str__(self):
        return str(self.id)

    def delete(self, **kwargs):
        self.deleted_on = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
