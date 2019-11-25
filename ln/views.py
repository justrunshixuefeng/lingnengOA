from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Role, Permission, Announcement
from utils.response_code import RET, error_map
from lingnengOA.settings import permissions_url
from .serializers import Announcementser
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
            mes['code'] = RET.PARAMERR
            mes['message'] = error_map[RET.PARAMERR]
        else:
            user = User.objects.get(name=name)
            if not user:
                mes['code'] = RET.USERERR
                mes['message'] = error_map[RET.USERERR]
            else:
                if user.password == password:
                    # 将当前用户id存入session
                    request.session['user_id'] = user.id
                    # 查找出当前用户的权限url和code存入列表
                    permissions_list = user.roles.filter(
                        permissions__url__isnull=False).values(
                            'permissions__title',
                            'permissions__url',
                        ).distinct()
                    for i in permissions_list:
                        permissions_url.append(permissions_list['url'])
                    mes['code'] = RET.OK
                    mes['message'] = error_map[RET.OK]
                else:
                    mes['code'] = RET.PWDERR
                    mes['message'] = error_map[RET.PWDERR]
        return Response(mes)


class Send_announcement(APIView):
    """
    公告反序列化入库
    content：公告内容
    title: 公告标题
    """
    def post(self, request):
        mes = {}
        title = request.data['title']
        content = request.data['content']
        user_id = request.session.get('user_id')
        if not user_id:
            mes['code'] = RET.ROLEERR
            mes['message'] = error_map[RET.ROLEERR]
            return Response(mes)
        data = {'title': title, 'content': content, 'user_id': user_id}
        u = Announcementser(data=data)
        if u.is_valid():
            u.save()
            mes['code'] = RET.OK
            mes['message'] = error_map[RET.OK]
        else:
            print(u.errors)
            mes['code'] = RET.DATAERR
            mes['message'] = error_map[RET.DATAERR]
        return Response(mes)


class Check_announcement(APIView):
    """
    公告序列化出库
    """
    def get(self, request):
        mes = {}
        a = Announcement.objects.all()
        an = Announcementser(instance=a, many=True)
        mes['code'] = RET.OK
        mes['message'] = an.data
        return Response(mes)
