from django.db import models
from account.models import Account

class Question(models.Model):
    author                  = models.ForeignKey(Account, on_delete=models.CASCADE)
    title                   = models.CharField(max_length=120, default='')
    body                    = models.TextField(default='')
    num_likes               = models.IntegerField(default=0)
    num_answers             = models.IntegerField(default=0)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
