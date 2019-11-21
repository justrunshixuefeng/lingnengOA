from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
# Create your views here.


class Login(APIView):
    """
    登录
    """
    def post(self, request):
        """
        name  账号
        password  密码
        """
        mes = {}
        name = request.data['name']
        password = request.data['password']
        if not all([name, password]):
            mes['code'] = 10010
            mes['message'] = '参数不全'
        else:
            user = User.objects.get(name=name)
            if not user:
                mes['code'] = 10011
                mes['message'] = '用户不存在'
            else:
                if user.password == password:
                    mes['code'] = 200
                    mes['message'] = '登录成功'
                else:
                    mes['code'] = 10013
                    mes['message'] = '密码错误'
        return Response(mes)
