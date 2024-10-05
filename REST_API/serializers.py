
from rest_framework import serializers
from .models import Kitten, Breed, Rating

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']

class KittenSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)  # Если нужно вернуть информацию о породе
    breed_id = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all(), source='breed', write_only=True)  # Для создания и обновления породы по ID
    age = serializers.IntegerField(read_only=True)  # Используем вычисляемое поле
    average_rating = serializers.FloatField(read_only=True)  # Средний рейтинг доступен только для чтения

    class Meta:
        model = Kitten
        fields = ['id', 'name', 'breed','breed_id', 'color','birth_date', 'age', 'description', 'owner', 'average_rating']
        read_only_fields = ['owner']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'value', 'user', 'kitten']
        read_only_fields = ['user', 'kitten']
