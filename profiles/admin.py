from django.contrib import admin
from .models import Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','height_cm','weight_kg','exercise_plans_count','nutrition_plans_count')
    search_fields = ('user__username','user__email')
    list_filter = ('exercise_plans__category','nutrition_plans__category')
    autocomplete_fields = ('user','exercise_plans','nutrition_plans')
    list_select_related = ('user',)
    filter_horizontal = ('exercise_plans','nutrition_plans')

    def exercise_plans_count(self, obj):
        return obj.exercise_plans.count()
    exercise_plans_count.short_description = 'Exercise plans'

    def nutrition_plans_count(self, obj):
        return obj.nutrition_plans.count()
    nutrition_plans_count.short_description = 'Nutrition plans'
