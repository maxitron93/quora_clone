from rest_framework import serializers
from question.models import Question

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     self.author = kwargs.pop('author')
    #     super().__init__(*args, **kwargs)
