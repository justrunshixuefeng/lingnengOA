from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Role, Permission, Announcement, Department, Leave
from utils.response_code import RET, error_map
from lingnengOA.settings import permissions_url
from .serializers import Announcementser, Departmentser, Roleser, Userser, Update_Userser, Leaveser
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
            try:
                user = User.objects.get(name=name)
            except:
                mes['code'] = RET.USERERR
                mes['message'] = error_map[RET.USERERR]
                return Response(mes)
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
                        permissions_url.append(i['permissions__url'])
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
        try:
            title = request.data['title']
            content = request.data['content']
        except:
            mes['code'] = RET.DATAERR
            mes['message'] = error_map[RET.DATAERR]
            return Response(mes)
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


class Announcement_content(APIView):
    """
    获取前端公告id,返回对应内容
    """

    def post(self, request):
        mes = {}
        title_id = request.data.get('title_id')
        try:
            announcement = Announcement.objects.get(pk=title_id)
        except:
            mes['code'] = RET.DBERR
            mes['message'] = error_map[RET.DBERR]
            return Response(mes)
        else:
            a = Announcementser(instance=announcement)
            mes['code'] = RET.OK
            mes['message'] = a.data
            return Response(mes)


class Offer_entering(APIView):
    """
    提供用户录入信息的可选部门和角色权限
    """

    def get(self, request):
        mes = {}
        role = Role.objects.all()
        r = Roleser(instance=role, many=True)
        department = Department.objects.all()
        d = Departmentser(instance=department, many=True)
        mes['code'] = RET.OK
        mes['role'] = r.data
        mes['department'] = d.data
        return Response(mes)


class Offer_userinfo(APIView):
    """
    获取到用户的信息，反序列化入库
    """

    def post(self, request):
        mes = {}
        data = request.data
        u = Userser(data=data)
        if u.is_valid():
            u.save()
            mes['code'] = RET.OK
            mes['message'] = error_map[RET.OK]
        else:
            print(u.errors)
            mes['code'] = RET.DESERIALIZATION
            mes['message'] = error_map[RET.DESERIALIZATION]
        return Response(mes)


class All_userinfo(APIView):
    """
    返回所有员工的信息
    """

    def get(self, request):
        mes = {}
        try:
            user = User.objects.all()
            u = Userser(instance=user, many=True)
        except:
            mes['code'] = RET.DBERR
            mes['message'] = error_map[RET.DBERR]
            return Response(mes)
        mes['code'] = RET.OK
        mes['message'] = u.data
        return Response(mes)


class Search_name(APIView):
    """
    模糊查询员工姓名,返回员工所有信息
    name 模糊查询名字
    """

    def get(self, request):
        mes = {}
        name = request.data['name']
        u = User.objects.filter(name__contains=name)
        if u:
            user = Userser(instance=u)
            mes['code'] = RET.OK
            mes['message'] = user.data
        else:
            mes['code'] = RET.USERERR
            mes['message'] = error_map[RET.USERERR]
        return Response(mes)


class Update_userinfo(APIView):
    """
    接收员工id,更改员工信息
    """

    def put(self, request):
        mes = {}
        user_id = request.data.get('user_id')
        try:
            user = User.objects.filter(pk=user_id)[0]
        except:
            mes['code'] = RET.USERERR
            mes['message'] = error_map[RET.USERERR]
            return Response(mes)
        u = Update_Userser(instance=user, data=request.data)
        try:
            if u.is_valid():
                u.save()
                mes['code'] = RET.OK
                mes['message'] = error_map[RET.OK]
            else:
                print(u.errors)
                mes['code'] = RET.DESERIALIZATION
                mes['message'] = error_map[RET.DESERIALIZATION]
                return Response(mes)
        except:
            mes['code'] = 40000
            mes['message'] = '工号已经存在'
        return Response(mes)


class Offer_leader(APIView):
    """
    提供抄送人选项
    """

    def get(self, request):
        """
        把所有部长和经理级别角色权限的员工返回
        """

        mes = {}
        # roles = Role.objects.filter(id__gt=1).user_roles
        user = User.objects.filter(roles__id__gt=1).distinct()
        u = Userser(instance=user, many=True)
        mes['code'] = RET.OK
        mes['message'] = u.data
        return Response(mes)


class Leave_api(APIView):
    """
    请假接口
    获取前台的请假数据，反序列化入库
    """

    def post(self, request):
        mes = {}
        user_id = request.session.get('user_id')
        data = request.data.copy()
        data['initiator_id'] = user_id
        print("data数据为：")
        print(data)
        l = Leaveser(data=data)
        if l.is_valid():
            try:
                l.save()
            except:
                mes['code'] = 40001
                mes['message'] = '反序列化出错'
                return Response(mes)
            mes['code'] = RET.OK
            mes['message'] = error_map[RET.OK]
        else:
            print(l.errors)
            mes['code'] = RET.DESERIALIZATION
            mes['message'] = error_map[RET.DESERIALIZATION]
            return Response(mes)
        return Response(mes)


class All_Leave(APIView):
    """
    返回所有的请假数据
    """

    def get(self, request):
        mes = {}
        l = Leave.objects.all()
        lea = Leaveser(instance=l, many=True)
        mes['code'] = RET.OK
        mes['message'] = lea.data
        return Response(mes)
