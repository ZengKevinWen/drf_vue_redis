from django.urls import path
from .views import *
urlpatterns = [
    # todo 中奖名单 奖品 活动 奖等级信息
    path('winning_list/', WininglistAPIView.as_view()),  # 中奖名单
    path('wining_activity/', WiningActivityAPIView.as_view()),  # 中奖活动
    path('wining_type/', WiningTypeAPIView.as_view()),  # 中奖等级对象的奖品
    path("wing_prize/", WiningPrizeAPIView.as_view()),  # 奖品列表及信息
    # todo 准备抽奖业务实现(建立 抽奖名单表 实现抽奖逻辑 实现购物车功能 )----暂时想起的
    path("lucky_draw_list/", LuckyDrawListAPIVIew.as_view()),   # 增加抽奖名单
    path("luck_draw/", LuckDrawAPIView.as_view()),  # 抽奖机制
]