from django.shortcuts import render
from django.http import HttpResponse
from .models import Question,Choice
from rest_framework import viewsets
from rest_framework import permissions
from polls.serializers import QuestionSerializer,ChoiceSerializer
# Create your views here.

#API endpoint for restFramework
class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed and edited
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the choice to be viewed and edited
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

def index(request):
    return HttpResponse("Hello World! Welcome to the Polls App")
def get_questions(request):
    return HttpResponse(Question.objects.all())
def detail(request,question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return HttpResponse(f"{question}")
def results(request,question_id):
    return HttpResponse(f"You're looking at the results of {question_id}")
def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
