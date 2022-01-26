from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
user_choices_type = ((1,"用户"),
                    (2,"VIP用户"),
                    (3,"管理员"))

class User(AbstractUser):
    mobile = models.CharField(unique=True, blank=False, max_length=20)
    # 头像  uoload_to=相对路径(不可以用绝对路径)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 用户描述
    user_desc = models.TextField(blank=True)
    # 角色
    choices_type = models.IntegerField(default=1,choices=user_choices_type)

    class Meta:
        db_table='db_UserInfo'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.username


    def Tel(self):
        return self.mobile



# from django.utils import timezone
#
#
# # 中奖详细
# class Win_Prize(models.Model):
#
#     prize_type = ((0, "特等奖"), (1, "一等奖"), (2, "二等奖"), (3, "三等级"))
#     state_type = ((1,"发货"), (2, "下单"), (3, "签收"), (4, "未签收"), (5, "运输"))
#
#     name = models.IntegerField("中奖等级", default=3, choices=prize_type, blank=True, null=True)
#     create_date = models.TimeField(default=timezone.now)
#     updata_date = models.TimeField(auto_now=True)
#     demo = models.CharField(max_length=200, verbose_name="备注")
#     state = models.IntegerField(default=2, choices=state_type, blank=True, null=True)
#     prize_user = models.ForeignKey("User", on_delete=models.CASCADE,verbose_name="中奖的用户", blank=True , null=True)
#
#     class Meta:
#         db_table = 'db_user_win_prize'
#         verbose_name = "用户中奖详细表"
#         verbose_name_plural = verbose_name
#
#
# # 活动
# class Activity(models.Model):
#
#     name = models.CharField(max_length=50, verbose_name="活动名称")
#     activity_start_date = models.TimeField(default=timezone.now, verbose_name="活动开始日期")
#     activity_end_date = models.TimeField(auto_now=True, verbose_name="获得结束日期")
#     demo = models.TextField()
#     activity_user_prize = models.ForeignKey("Prize", on_delete=models.CASCADE, verbose_name="用户在那个活动中的奖",blank=True, null=True)
#
#     class Meta:
#         db_table = "db_activity"
#         verbose_name = "活动"
#         verbose_name_plural = verbose_name
#
#
# # 奖品
# class Prize(models.Model):
#
#     name = models.CharField(max_length=20, verbose_name="奖品名称")
#     money = models.CharField(max_length=20, verbose_name="价格")
#     demo = models.TextField()
#     prize_activity = models.ForeignKey("Activity", on_delete=models.CASCADE, null=True, blank=True)
#     prize_win_prize = models.ForeignKey(Win_Prize, on_delete=models.CASCADE, blank=True, null=True)
#
#     class Meta:
#         db_table = "db_prize"
#         verbose_name = '奖品表'
#         verbose_name_plural = verbose_name