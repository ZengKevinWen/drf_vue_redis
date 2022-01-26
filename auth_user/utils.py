from datetime import datetime, timezone
import json
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import *
from .auth import logger  # 日志对象
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import django_redis
# todo jtw生成token
import jwt

class  JWTToken(object):
    def __init__(self,conntent,algorithm=None):
        self.select_keys = settings.SECRET_KEY   # 盐
        self.pyload = self.pyload(conntent)
        if algorithm is None:
            self.algorithm = "HS256"
        else:
            self.algorithm = algorithm

    def create_token(self):
        # todo 很奇怪 在加密的时候要加decode转化为字符串类型后 在解码时不需要进行decode(而有些博客要解除---自己感觉可以是版本的问题)
        token = jwt.encode(payload=self.pyload, key=self.select_keys, algorithm=self.algorithm).decode()
        print(token)
        return token
    # 对载荷进行配置时间zhuo
    def pyload(self,content):
        # content["exp"] =datetime.now(tz=timezone.utc)  # todo 这里有个问题 在encode时加上时间zhuo时在解密时报错 解密失败 这个问题还没有解决！！！！！！！！！！1
        print(content)
        # content_1 = json.dumps(content)
        # print(content_1)
        return content

# todo 解密token
def check_token(token):
    # 解码
    print("token解密")
    if token:
        print(1111)
        user_obj = User()   # 有点问题
        print(token)
        try:
            decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user_obj = User.objects.get(id=int(decoded["id"]))
            # token_ = jwt.decode(token, key=settings.SECRET_KEY,algorithms="HS256")
            # 寻找匹配user对象
        except Exception as e:
            # settings.logger.error(e)
            raise AuthenticationFailed({"message":"用户登录异常，请重新登录"})
        return user_obj,token  # user对象，token
    # return


# todo 节流
from django_redis import get_redis_connection
from rest_framework.throttling import BaseThrottle

class MyThrottle(BaseThrottle):

    def allow_request(self, request, view):

        user = request.user
        try:
            redis_conn = get_redis_connection("throttle")
            user_throtting = redis_conn.get("%d:%s" % (user.id, user.username))
            print(type(user_throtting))
            print(user_throtting)
            # print(type(user_throtting.decode('utf-8')))
            # print(user_throtting.decode('utf-8'))
            # todo 有点瑕疵  因为第一次节流时 是Nonetype类型 无法进行decode操作  所有要先判断才可以进行操作 如果对Nonetype进行decode操作会报错 2个if
            if user_throtting:
                user_throtting = user_throtting.decode()
                if int(user_throtting) >= 5:
                    return False
                else:
                    redis_conn.incr("%d:%s" % (user.id, user.username))
                    return True
            else:
                redis_conn.setex("%d:%s" % (user.id, user.username), 60, 1)
                return True
        except Exception as e:
            logger.error(e, "redis存储错误")
            return Response({"message": "Redis存储错误,请稍后再试"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)



    def wait(self):
        return 60


from ronglian_sms_sdk import SmsSDK
class SendMessage_(object):

    def __init__(self, accId, accToken, appId):
        '''
        :param accId: 容联云通讯分配的主账号ID
        :param accToken: 容联云通讯分配的主账号TOKE
        :param appId: 容联云通讯分配的应用ID
        '''
        self.accId = accId
        self.accToken = accToken
        self.appId = appId

    def send_message(self, tid, mobile, datas):
        '''
        :param tid: 容联云通讯创建的模板ID
        :param mobile:  手机号1,手机号2
        :param datas:  ('变量1--验证码', '变量2---时间')
        :return:
        '''
        sdk = SmsSDK(self.accId, self.accToken, self.appId)
        # 保存验证码存入redis中
        self.save_message(datas=datas, mobile=mobile)
        # 发送短信
        resp = sdk.sendMessage(tid, mobile, datas)
        print(resp)

    # 保存验证码存入redis中
    def save_message(self, datas, mobile):
        try:
            # 链接redis
            redis_conn = django_redis.get_redis_connection("message")
            # 操作redis
            redis_conn.setex("%s:mobile" % mobile, datas[1]*60, datas[0])
        except Exception as e:
            logger.error(e)
            print(dir(e))
            return Response({"message": "redis存储报错"},status=status.HTTP_507_INSUFFICIENT_STORAGE)



# todo 对验证码数据就行校验
def verification_message(mobile, message):
    try:
        # 链接redis
        redis_conn = django_redis.get_redis_connection("message")
        # 操作redis
        # todo 157手机
        print(mobile)
        message_ = redis_conn.get("%s:mobile" % '15773998780').decode()
    except Exception as e:
        logger.error(e)
        print(dir(e))
        return Response({"message": "redis存储报错"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        # 过期或者不存在
    if not message_ :
        return None
        # 验证码正确或者错误
    if message == message_ :
        # 删除验证码
        return True
    else:
        return False