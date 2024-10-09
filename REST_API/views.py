from rest_framework import generics, permissions
from .models import Kitten, Breed, Rating
from .serializers import KittenSerializer, BreedSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters


class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class KittenListView(generics.ListCreateAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("breed",) # набор полей для фильтрации

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class KittenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Пользователь может изменять/удалять только своих котят
        return Kitten.objects.filter(owner=self.request.user)


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Получаем котенка по переданному ID
        kitten_id = self.kwargs.get('kitten_id')
        kitten = get_object_or_404(Kitten, pk=kitten_id)

        # Проверяем, если уже есть оценка от этого пользователя
        if Rating.objects.filter(user=self.request.user, kitten=kitten).exists():
            raise ValidationError("Вы уже оценили этого котенка.")

        serializer.save(user=self.request.user, kitten=kitten)


class KittenRatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        kitten_id = self.kwargs.get('kitten_id')
        return Rating.objects.filter(kitten__id=kitten_id)


