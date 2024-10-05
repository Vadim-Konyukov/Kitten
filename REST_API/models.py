from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название породы',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

class Kitten(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода котенка')
    name = models.CharField(max_length=255, verbose_name='Имя котенка',)
    color = models.CharField(max_length=55, verbose_name='Цвет котенка')
    birth_date = models.DateField(verbose_name='Дата рождения котенка')
    description = models.TextField(verbose_name='Описание котенка')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Владелец')

    @property
    def age(self):
        today = timezone.now().date()
        # Проверяем разницу в днях
        delta = today - self.birth_date

        # Если разница в днях меньше 30, возвращаем 0
        if delta.days < 30:
            return 0

        age_years = today.year - self.birth_date.year
        age_months = today.month - self.birth_date.month

        # Если текущий день месяца меньше дня рождения, вычитаем 1 месяц
        if today.day < self.birth_date.day:
            age_months -= 1

        # Возвращаем полные месяцы
        return age_years * 12 + age_months

    def average_rating(self):
        ratings = self.ratings.all()  # получаем все оценки котенка
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0

    def __str__(self):
        return self.name

class Rating(models.Model):
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Оценки от 1 до 5
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kitten = models.ForeignKey(Kitten, related_name='ratings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'kitten')  # Один пользователь может поставить одну оценку одному котенку

    def __str__(self):
        return f'{self.user} оценил {self.kitten} на {self.value}'