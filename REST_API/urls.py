from django.urls import path
from .views import BreedListView, KittenListView, KittenDetailView, RatingCreateView, KittenRatingListView


urlpatterns = [
    path('breeds/', BreedListView.as_view(), name='breed-list'),
    path('kittens/', KittenListView.as_view(), name='kitten-list'),
    path('kittens/<int:pk>/', KittenDetailView.as_view(), name='kitten-detail'),
    path('kittens/<int:kitten_id>/rate/', RatingCreateView.as_view(), name='kitten-rate'),
    path('kittens/<int:kitten_id>/ratings/', KittenRatingListView.as_view(), name='kitten-rating-list'),

]
