from . import models
from rest_framework import serializers

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Question
        fields = ['question_text','pub_date']

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Choice
        fields = ['choice_text','votes']