from django.contrib import admin
from question.models import Question

# Register your models here.
admin.sites.regster(Question)