from django.contrib import admin

from .models import User, Diet, Food, Profile, MealPlan, Nutrition, Submission

admin.site.register(User)
admin.site.register(Diet)
admin.site.register(Food)
admin.site.register(Profile)
admin.site.register(MealPlan)
admin.site.register(Nutrition)
admin.site.register(Submission)
