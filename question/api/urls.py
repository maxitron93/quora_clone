from django.urls import path
from question.api.views import CreateListMyQuestions, ListAllQuestions, RUDQuestion

urlpatterns = [
    path('', CreateListMyQuestions.as_view(), name='my_questions'),
    path('all', ListAllQuestions.as_view(), name='list_all_questions'),
    path('<int:pk>', RUDQuestion.as_view(), name='RUD_question')
]
