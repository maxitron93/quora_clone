from rest_framework.views import APIView
from question.models import Question
from question.api.serializers import QuestionSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404

# Returns all the questions
class ListAllQuestions(APIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

# Returns all the user's questions
# Allows user to create a question
class CreateListMyQuestions(APIView):

    permission_classes = [permissions.IsAuthenticated]

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

# Create custom permission similar to IsOwnerOrReadOnly
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow author of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return False
        # Instance must have an attribute named `author`.
        else:
            return obj.author == request.user

# Get specific question
# Allow user to update specific question
# Allow user to delete specific question
class RUDQuestion(APIView):

    permission_classes = [IsAuthorOrReadOnly]

    def get_question_or_404(self, pk):
        question = get_object_or_404(Question, pk=pk)
        return question

    def get(self, request, pk):
        question = self.get_question_or_404(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk):
        question = self.get_question_or_404(pk=pk)
        self.check_object_permissions(request, question) # Need to add this after getting to object to check for permission
        serialized = QuestionSerializer(question, data=request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = self.get_question_or_404(pk=pk)
        self.check_object_permissions(request, question)  # Need to add this after getting to object to check for permission
        question.delete()
        return Response({'message': 'Question deleted'}, status=status.HTTP_200_OK)
