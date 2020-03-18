from rest_framework.views import APIView
from question.models import Question
from question.api.serializers import QuestionSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CreateListMyQuestions(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        questions = Question.objects.filter(author=user.id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        author_id = request.user.id
        data['author'] = author_id
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

