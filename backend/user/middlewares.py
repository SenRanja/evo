# encoding=utf-8
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from conf.errors import error_unauth_msg


# 没有认证，就拒绝服务
class AuthCookie(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated and (request.path not in ("/api/login/", "/api/register/")):
            return JsonResponse(error_unauth_msg(), status=401)

    # def process_response(self, request, response):
    #     # 基于请求响应
    #     print("md1  process_response 方法！", id(request))  # 在视图之后
    #     return response
    #
    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print("md1  process_view 方法！")  # 在视图之前执行 顺序执行
    #     # return view_func(request)
    # def process_exception(self, request, exception):    #引发错误 才会触发这个方法
    #     print("md1  process_exception 方法！")
    #     # return HttpResponse(exception, status="404")
