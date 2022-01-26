
import django_redis
import logging

from rest_framework.response import Response
from rest_framework import status

from app.models import LuckDraw, Win_Prize, LotteryRecord

logger = logging.getLogger("django")


# 抽奖业务实现
class PrizeOptions(object):

    def __init__(self):
        self.prize_redis_conn = django_redis.get_redis_connection("prize")

    def insert(self, prize_list):
        # 设置 set类型 同时删除LuckDraw表中数据 增加LotteryRecord 表中数据
        for prize in prize_list:
            prize_id = prize.id
            # todo =======================================================
            print(prize_id)
            print(prize)
            print(prize.demo)
            print(prize.luckdraw_activity)  # todo 这里有一些问题 按道理来说 这里应该是数值 而删除的是 Object对象 ---------------------------- 因为在activity模型类中 没有设置 __str__函数
            print(prize.luckdraw_activity.id)
            print(prize.luckdraw_activity.name)
            # todo ===========================================================
            # todo 增加 抽奖记录表
            obj = LotteryRecord()
            obj.id = prize.id
            obj.demo = "测试"
            obj.lotteryrecord_activity_id = prize.luckdraw_activity_id
            obj.lotteryrecord_user_id = prize.luckdraw_user_id
            obj.save()
            try:
                self.prize_redis_conn.sadd("%s:activity" % prize.luckdraw_activity.id, prize_id )
                print(prize_id)
            except Exception as e:
                logger.error(e)
                return Response({"message": "redis存储错误"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
            # todo 然后 删除 抽奖名单中的数据
            prize.delete()
        print("完成")

    def destory(self, activity_id):
        # 获取抽奖名单
        # todo spop key （取出key中某个数据并移除key中）
        try:
            prize_id = self.prize_redis_conn.spop("%s:activity" % activity_id).decode()
            # 删除抽奖set类型
            try:
                # 对中奖进行 Win_Prize表中存储
                print(type(prize_id))
                prize_ = LotteryRecord.objects.get(id=prize_id)
                obj = Win_Prize()
                obj.demo = "测试"
                obj.win_prize_activity = prize_.lotteryrecord_activity
                obj.prize_user = prize_.lotteryrecord_user
                obj.save()
            except Win_Prize.DoesNotExist as e:
                logger.error(e)
                return Response({"message": "mysql错误"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        except Exception as e:
            logger.error(e)
            return Response({"message": "redis存储错误"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        print("完成")
        return str(obj.id)
