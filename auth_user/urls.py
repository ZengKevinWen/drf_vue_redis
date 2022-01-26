from django.urls import path
from .views import *
urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('Permssions/', Permssions.as_view()),  # 权限
    path("user_info_options/", MyRetrieveUpdateDestroyAPIView.as_view()),  # 用户信息
    path("register_list/", MyRegisterListAPIView.as_view()),  # drf注册
    path("send_message/", SendMessage),  # 发送短信
    path("register/", MyRegisterAPIView.as_view()),   # 实现第三方平台功能的注册
]