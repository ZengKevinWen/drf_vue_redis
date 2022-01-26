from django.db import models

# Create your models here.
from django.utils import timezone
from auth_user.models import User

# 中奖名单详细
class Win_Prize(models.Model):

    # prize_type = ((0, "特等奖"), (1, "一等奖"), (2, "二等奖"), (3, "三等级"))
    state_type = ((1,"发货"), (2, "下单"), (3, "签收"), (4, "未签收"), (5, "运输"))
    # name = models.IntegerField("中奖等级", default=3, choices=prize_type, blank=True, null=True)
    create_date = models.TimeField(default=timezone.now)
    updata_date = models.TimeField(auto_now=True)
    demo = models.CharField(max_length=200, verbose_name="备注")
    state = models.IntegerField(default=2, choices=state_type)  # 这里应该写错了  没有实现
    prize_user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="中奖的用户", blank=True , null=True)
    win_prize_activity = models.ForeignKey("Activity", on_delete=models.CASCADE, verbose_name="属于那个活动", blank=True, null=True)
    prize_type = models.ForeignKey("Prize_type", on_delete=models.CASCADE, blank=True, null=True, verbose_name="中奖等级名称")

    class Meta:
        db_table = 'db_user_win_prize'
        verbose_name = "用户中奖详细表"
        verbose_name_plural = verbose_name


# 活动
class Activity(models.Model):

    name = models.CharField(max_length=50, verbose_name="活动名称")
    activity_start_date = models.TimeField(default=timezone.now, verbose_name="活动开始日期")
    activity_end_date = models.TimeField(auto_now=True, verbose_name="获得结束日期")
    demo = models.TextField()
    # activity_user_prize = models.ForeignKey("Prize", on_delete=models.CASCADE, verbose_name="用户在那个活动中的奖",blank=True, null=True)

    class Meta:
        db_table = "db_activity"
        verbose_name = "活动"
        verbose_name_plural = verbose_name


# 奖分类
class Prize_type(models.Model):

    name = models.CharField(max_length=20,verbose_name="奖的名称")
    create_date = models.TimeField(default=timezone.now)
    update_date = models.TimeField(auto_now=True)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,verbose_name="奖所属的活动")

    class Meta:
        db_table = 'db_prize_type'
        verbose_name = "奖分类"
        verbose_name_plural = verbose_name


# 奖品
class Prize(models.Model):


    name = models.CharField(max_length=20, verbose_name="奖品名称", unique=True)
    money = models.CharField(max_length=20, verbose_name="价格", blank=True, null=True)
    demo = models.TextField(blank=True, null=True)
    # prize_activity = models.ForeignKey("Activity", on_delete=models.CASCADE, null=True, blank=True)
    prize_win_prize = models.ForeignKey(Prize_type, on_delete=models.CASCADE, blank=True, null=True)  # todo 这个unique要注意 ；理解

    class Meta:
        db_table = "db_prize"
        verbose_name = '奖品表'
        verbose_name_plural = verbose_name


#  抽奖名单
class  LuckDraw(models.Model):

    # todo 以后时间用DateTime字段 可以减少报错
    create_date = models.DateTimeField(default=timezone.now, verbose_name="穿件时间", blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    demo = models.TextField(blank=True)
    luckdraw_activity = models.ForeignKey("Activity", on_delete=models.CASCADE, blank=True, null=True)
    # 　todo 这里设计有问题  因为 这里luckdraw_activity  luckdraw_prize_type  可能并不是 一对多关系
    # luckdraw_prize_type = models.ForeignKey("Prize_type", on_delete=models.CASCADE, blank=True, null=True)
    luckdraw_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)



#   抽奖记录
class LotteryRecord(models.Model):

    create_date = models.DateTimeField(default=timezone.now, verbose_name="创建时间", blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    demo = models.TextField(blank=True)
    lotteryrecord_activity = models.ForeignKey("Activity", on_delete=models.CASCADE, blank=True, null=True)
    lotteryrecord_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'db_lotteryrecord'
        verbose_name = "抽奖记录"
        verbose_name_plural = verbose_name