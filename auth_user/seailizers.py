
from .models import User
from rest_framework.serializers import ModelSerializer




# todo User序列化器
class LoginSearializers(ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"


class UserSerializers(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"