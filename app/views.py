from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import WininglistSerailizers, WiningActivitySerializers, WiningTypeSerailizers, WiningPrizeSerializers, LuckyDrawListSerializers
from auth_user.auth import MyAuthentication
import django_redis
# 中奖名单
class WininglistAPIView(ListAPIView):
    authentication_classes = [MyAuthentication, ]
    # queryset = Win_Prize.objects.all().order_by('-id', '-create_date')[:9]
    serializer_class = WininglistSerailizers

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        id = request._request.GET.get("demo", 0)
        if id == 0:
            queryset = Win_Prize.objects.all().order_by('-id', '-create_date')[:9]
        else:
            user = request.user
            queryset = Win_Prize.objects.filter(prize_user=user.id).order_by('-id', 'create_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# 活动
class WiningActivityAPIView(ListAPIView):

    serializer_class = WiningActivitySerializers
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        activity_id = request._request.GET.get("activity", 1)
        if activity_id == 1:
            queryset = Activity.objects.get(id=activity_id)
            print(type(queryset))
            serializer = self.get_serializer(queryset)  # todo 这里可以增加inintance方法来判断 queryset是什么类型  从而many=？ 则不需要2次序列化
        else:
            queryset = Activity.objects.all().order_by('-id')
            print(type(queryset))
            serializer = self.get_serializer(queryset, many=True)
        # if isinstance()   todo 这里可以增加inintance方法来判断 queryset是什么类型  从而many=？ 则不需要2次序列化
        return Response(serializer.data)


# 等级
class WiningTypeAPIView(ListAPIView):
    serializer_class = WiningTypeSerailizers

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        activity_id = request._request.GET.get("activity", 1)
        activity = Activity.objects.get(id=activity_id)
        activity_prize_type = activity.prize_type_set.all()
        serializer = self.get_serializer(activity_prize_type, many=True)
        return Response(serializer.data)


class WiningPrizeAPIView(ListCreateAPIView):
    queryset = Prize.objects.all()
    serializer_class = WiningPrizeSerializers


# 增加抽奖名单  列表抽奖名单
class LuckyDrawListAPIVIew(ListCreateAPIView):

    queryset = LuckDraw.objects.all()
    serializer_class = LuckyDrawListSerializers


# todo 抽奖操作   还没有实现
from .utlis import PrizeOptions
class LuckDrawAPIView(APIView):

    authentication_classes = [MyAuthentication, ]

    # 抽奖业务 实现
    def get(self,request):
        activity_id = request.data.get("activity", "1")
        prize_list = LuckDraw.objects.filter(luckdraw_activity=activity_id)[:10]
        print(prize_list)
        # todo 这里尝试用Redis中的set类型· 实现抽奖业务
        obj = PrizeOptions()
        obj.insert(prize_list)
        p = obj.destory(activity_id)
        pz = Win_Prize.objects.get(id=int(p))
        serializers = WininglistSerailizers(instance=pz)
        return Response(serializers.data)


from rest_framework.views import exception_handler
class Test(APIView):
    def get(self,request):
        pass



