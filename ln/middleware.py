from django.utils.deprecation import MiddlewareMixin
import re
from lingnengOA.settings import WHITE_URL, permissions_url
from django.http import JsonResponse
from utils.response_code import error_map, RET


class RBACMiddle(MiddlewareMixin):
    def process_request(self, request):
        mes = {}
        # 1,匹配请求的url是否在白名单中
        u = request.path
        for i in WHITE_URL:
            if re.match(i, u):
                # 不做任何事，返回空
                return None
        # 2,查看当前用户是否登录，查看session
        user_id = request.session.get('user_id')
        if not user_id:
            mes['code'] = RET.SESSIONERR
            mes['message'] = error_map[RET.SESSIONERR]
            return JsonResponse(mes)
        # 3,当前路由是否在用户的权限url列表里
        per = ('^{0}$'.format(u))
        flag = False
        for i in permissions_url:
            if re.match(per, i):
                flag = True
                # break
                return None
        if not flag:
            mes['code'] = RET.PERMISSION
            mes['message'] = error_map[RET.PERMISSION]
            return JsonResponse(mes)
