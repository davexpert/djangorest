from rest_framework import serializers
from . import models

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = "id title duration".split()
        # fields = "__all__"

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"
