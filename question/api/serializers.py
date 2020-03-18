from rest_framework import serializers
from question.models import Question

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['num_likes', 'num_answers', 'create_at', 'updated_at']
