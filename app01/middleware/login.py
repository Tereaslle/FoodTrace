from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from django.contrib import messages

class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return
        if request.path_info.find("esp32") != -1:
            return
        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            if info_dict['type_name'] == '超级管理员':
                return
            elif info_dict['type_name'] == '企业级管理员':
                if request.path_info.find("enterprise") != -1:
                    print(f"当前访问域名{request.path_info}  用户身份:{info_dict['type_name']} 状态:禁止访问，已拦截")
                    # if not messages:
                    # messages.error(request, '当前用户无权访问') # 在layout页面中加入模版语法显示错误信息
                    return redirect("/user/list/")
                else:
                    print(f"当前访问域名{request.path_info}  用户身份:{info_dict['type_name']} 状态:允许访问")
                    return
            else:
                # messages.error(request, '未标识的权限用户，请重新登陆')
                return redirect('/login/')

        # 2.没有登录过，重新回到登录页面
        messages.error(request, '当前用户无权访问')  # 在layout页面中加入模版语法显示错误信息
        return redirect('/login/')
