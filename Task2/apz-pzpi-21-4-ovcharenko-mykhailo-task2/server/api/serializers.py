from django.http.response import json
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Food, Nutrition, Profile, User
from .utils.lang import Lang


class UserSerializer(ModelSerializer):
    role = SerializerMethodField()

    def __init__(self, lang: Lang, data):
        self._lang = lang
        super().__init__(data)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "weight",
            "body_fat",
            "role",
            "date_of_birth",
            "created_at",
            "last_seen_at",
        ]

    def get_role(self, obj: User):
        return {"id": obj.role, "name": self._lang.translate(f"role.{obj.role}")}


class NutritionSerializer(ModelSerializer):
    vitamins = SerializerMethodField()
    minerals = SerializerMethodField()
    amino_acids = SerializerMethodField()

    def __init__(self, lang: Lang, data):
        self._lang = lang
        super().__init__(data)

    class Meta:
        model = Nutrition
        fields = [
            "nutrition_id",
            "vitamins",
            "minerals",
            "amino_acids",
        ]

    @staticmethod
    def get_vitamins(obj: Nutrition):
        return json.loads(obj.vitamins)  # type: ignore

    @staticmethod
    def get_minerals(obj: Nutrition):
        return json.loads(obj.minerals)  # type: ignore

    @staticmethod
    def get_amino_acids(obj: Nutrition):
        return json.loads(obj.amino_acids)  # type: ignore


class ProfileSerializer(ModelSerializer):
    diet = SerializerMethodField()
    nutrition = SerializerMethodField()
    user = SerializerMethodField()

    def __init__(self, lang: Lang, data):
        self._lang = lang
        super().__init__(data)

    class Meta:
        model = Profile
        fields = [
            "profile_id",
            "preferences",
            "diet",
            "nutrition",
            "user",
        ]

    @staticmethod
    def get_diet(obj: Profile):
        return None

    def get_nutrition(self, obj: Profile):
        return NutritionSerializer(self._lang, obj.fk_nutrition).data

    def get_user(self, obj: Profile):
        return UserSerializer(self._lang, obj.fk_user).data


class FoodSerializer(ModelSerializer):
    nutrition = SerializerMethodField()

    def __init__(self, lang: Lang, data):
        self._lang = lang
        super().__init__(data)

    class Meta:
        model = Food
        fields = [
            "food_id",
            "name",
            "description",
            "photo_url",
            "carbs",
            "protein",
            "fat",
            "calories",
            "nutrition",
        ]

    def get_nutrition(self, obj: Profile):
        return NutritionSerializer(self._lang, obj.fk_nutrition).data