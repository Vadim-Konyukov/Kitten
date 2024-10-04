
from rest_framework import serializers
from .models import Kitten, Breed, Rating

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']

class KittenSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Kitten
        fields = ['id', 'name', 'breed', 'color', 'age', 'description', 'owner', 'average_rating']
        read_only_fields = ['owner']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'value', 'user', 'kitten']
        read_only_fields = ['user', 'kitten']
