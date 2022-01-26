from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .auth import MyAuthentication
from .utils import MyThrottle
from django.http import JsonResponse
import logging
logger = logging.getLogger("django")


class LoginAPIView(APIView):
    authentication_classes = [MyAuthentication, ]
    throttle_classes = [MyThrottle, ]

    def get(self,request):
        # self.dispatch()
        print(request.user)
        print(request.auth)
        return Response({"message":"登录成功",'token':request.auth},status=status.HTTP_200_OK)
        # return HttpResponse({"message":"登录成功"},status=status.HTTP_200_OK)


from .models import User
# todo 需要权限才可以访问的数据  ---这里先初始的排判断
from .seailizers import LoginSearializers
from .perssions import MyPerssions
class Permssions(ListAPIView):
    # self.dispatch
    throttle_classes = [MyThrottle, ]
    # permission_classes = [MyPerssions,]
    authentication_classes = [MyAuthentication, ]
    queryset = User.objects.all()
    serializer_class = LoginSearializers




# 注册 数据列表
from .seailizers import UserSerializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
class MyRegisterListAPIView(ListCreateAPIView):

    serializer_class = UserSerializers
    queryset = User.objects.all()


# todo 调用该模型类时  要增加一个  lookup_url_kwarg类型有关  要重新刷drf源码才看解决----------------尚未解决
# todo 最简单的注册用户　　　第三方操作都　没有的
class MyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializers
    queryset = User.objects.get(id=1)

import re
# todo 增加短信验证码 容联云的操作
class MyRegisterAPIView(APIView):
    serializer_class = UserSerializers

    def post(self, request):
        # 获取数据
        mobile = request.data.get("mobile")
        username = request.data.get("username")
        message = request.data.get("message")
        password = request.data.get("password")
        try:
            if not re.match(r'^1[3-9]\d{9}$', mobile):
                raise ValueError({"message": "请输入正确手机号"})
            # if User.objects.get(mobile=mobile) is None:  todo 在后面的反系列化时 会对手机号 username 密码等进行is_valid()方法
            #     raise ValueError({"message": "手机号已被注册, 请重新输入手机号"})
            if not re.match(r'^[0-9a-zA-Z]{8,20}$', password):
                raise ValueError({"message": "请输入要求的密码"})
            # 短信校验
            from .utils import verification_message
            message_hadler = verification_message(mobile=mobile, message=message)
            if message_hadler == None:
                return Response({"message": "验证码过期或者不存在"})
            elif message_hadler == False:
                return Response({"message": "验证码错误"})
            else:
                #todo  注册用户  系列化数据生成----使用drf源码为基础  修改了部分代码
                print("增加用户")
                # from rest_framework.generics import CreateAPIView
                # obj = CreateAPIView()
                serializer = UserSerializers(data=request.data)
                if not serializer.is_valid(): # is_valid方法是系列化中的方法
                    return JsonResponse(serializer.errors)
                serializer.save()   # todo 首先要对系列化后的数据就行校验才 可以进行save() 保存
                # 返回结果
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(dir(e))
            logger.error(e)
            print(e)  #  ERROR views 81 {'message': 'xxxxxxxxxxxxxxxxx'}  要去处前面的数据才可以就行系列化
            # print(json.dumps(e))
            return HttpResponse(e)


# 发送短信
from .utils import SendMessage_
import random
def SendMessage(request):
    mobile = request.GET.get("mobile")
    print(mobile)
    id = '8a216da87c304531017c6a4cebe50718'
    token = '9d9886d1765643a392e81261601d27a3'
    appid = '8a216da87c304531017c6a4cece3071f'
    obj = SendMessage_(accToken=token, accId=id, appId=appid)
    tid = 1
    # 生成6为数值
    string = "%06d" % random.randint(0, 999999)
    # 验证码时效 time
    time = 60
    datas = (string, time)
    obj.send_message(tid=tid, mobile='15773998780', datas=datas)  # todo 联容云没有注册别的手机好   所有这里还是用157开头的发送短信 同时在校验时也要用157的
    return HttpResponse({"message": "发送成功"}, status=status.HTTP_200_OK)