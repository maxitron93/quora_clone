from django.urls import path
from question.api.views import CreateListMyQuestions

urlpatterns = [
    path('', CreateListMyQuestions.as_view(), name='my_questions')
]