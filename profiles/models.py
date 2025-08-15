from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    goals = models.TextField(blank=True)
    exercise_plans = models.ManyToManyField('catalog.Product', blank=True, related_name='exercise_profiles', limit_choices_to={'category__slug': 'exercise'})
    nutrition_plans = models.ManyToManyField('catalog.Product', blank=True, related_name='nutrition_profiles', limit_choices_to={'category__slug': 'nutrition'})

    def __str__(self):
        return f"Profile({self.user.username})"

    def get_absolute_url(self):
        return reverse('profile_me')