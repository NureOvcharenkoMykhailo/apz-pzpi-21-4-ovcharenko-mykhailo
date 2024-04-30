from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User
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
