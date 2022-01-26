from rest_framework import serializers
from .models import *


class WininglistSerailizers(serializers.ModelSerializer):

    class Meta:

        model = Win_Prize
        fields = ['prize_user', 'win_prize_activity', 'prize_type']
        depth = 2


class WiningActivitySerializers(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = "__all__"
        depth = 2



class WiningTypeSerailizers(serializers.ModelSerializer):

    class Meta:
        model = Prize_type
        fields = "__all__"
        depth = 2


class WiningPrizeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = "__all__"
        depth = 3


class LuckyDrawListSerializers(serializers.ModelSerializer):
    mycreate_date = serializers.DateTimeField(source="create_date", read_only=True)
    myupdate_date = serializers.DateTimeField(source="update_date", read_only=True)

    class Meta:
        model = LuckDraw
        fields = "__all__"