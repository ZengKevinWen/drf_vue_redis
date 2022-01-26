from rest_framework import status, exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
# 日志
import logging
logger = logging.getLogger("django")

from .models import User
import base64
from django.contrib.auth.hashers import check_password
from .utils import JWTToken,check_token
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # todo 先校验是否有token
        token = request.query_params.get("token")
        check_token_ = check_token(token)
        if not check_token_:
            user = request.query_params.get("username", None)
            password = request.query_params.get("password", None)
            # password = check_password(password=password,encoded=base64.decode) # todo 这里还需要修改 把输入的密码加密与sql中的密码进行比较
            try:
                user_obj = User.objects.filter(username=user).first()
                if user_obj:
                    if not user_obj.password == password:
                        # return Response({"message":"密码错误"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
                        raise exceptions.AuthenticationFailed("密码错误")
                else:
                    raise exceptions.AuthenticationFailed({"message":"账号或者用户错误","code":"10001"})
            except User.DoesNotExist as e:
                logger.error(e)
                raise exceptions.AuthenticationFailed("用户名错误")
            # todo 实现jwt中token生成
            content = {"id":user_obj.id,"username":user_obj.username}
            print(content)
            token = JWTToken(content).create_token()
            user_obj.token = token
        else:
            print(check_token_)
            user_obj, user_obj.token = check_token_
        return (user_obj, user_obj.token)



from rest_framework.permissions import BasePermission
# class MyAuthentication(Ba)