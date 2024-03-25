# encoding=utf-8

from log.loguru_log import log_debug, log_data

__doc__ = '''错误代码
三位数代码，如200,401,404 依据常见HTTP请求问题响应。
自定义错误为四位数代码，从1000起始响应。

常见的HTTP响应码及其含义：

    1xx（信息性状态码）:
        100 Continue: 服务器已收到请求头，并且客户端应继续发送请求体。
        101 Switching Protocols: 服务器已经理解了客户端的请求，通过Upgrade消息头通知客户端切换协议。

    2xx（成功状态码）:
        200 OK: 请求成功。
        201 Created: 请求已经被实现，新的资源已经依据请求的需要而建立。
        204 No Content: 服务器成功处理了请求，但不需要返回任何实体内容。

    3xx（重定向状态码）:
        301 Moved Permanently: 请求的资源已被永久移动到新位置。
        302 Found: 请求的资源临时从不同的URI响应请求。
        304 Not Modified: 自从上次请求后，请求的资源未被修改过。

    4xx（客户端错误状态码）:
        400 Bad Request: 服务器无法理解请求的格式，通常由于请求中包含了无效的参数。
        401 Unauthorized: 请求要求用户的身份认证。
        403 Forbidden: 服务器理解请求，但拒绝执行它。

    5xx（服务器错误状态码）:
        500 Internal Server Error: 服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。
        502 Bad Gateway: 服务器作为网关或代理，从上游服务器收到了无效的响应。
        503 Service Unavailable: 服务器目前无法使用（由于超载或停机维护等原因）。'''

# 无错误

def success_msg(msg):
    return {"err_code": 0, "msg": msg, }

# json请求格式出错
def error_json_format(msg):
    return {"err_code": 1, "msg": msg, }

# 未授权访问
def error_unauth_msg():
    return {"err_code": 401, "msg": "unauth", }

# [user]
# 注册、登录、登出功能报错
def error_log_msg(msg):
    return {"err_code": 1000, "msg": msg, }

# 被禁用用户在登录
def error_no_active_user_login_msg(request, msg):
    err_code = 1001
    log_debug.error(msg)
    return {"err_code": err_code, "msg": msg, }

# excel文件导入用户失败
def error_excel_import_user_msg(request,msg:str):
    err_code = 1002
    err_msg = "user:{id}:{name} err_code:{err_code} err_msg:{err_msg}".format(id=request.user.id, name=request.user.name, err_code=err_code,err_msg=msg)
    log_debug.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }



# [group]
# 注册group重名
def error_duplicate_group_add_msg(err:str):
    err_code = 2000
    err_msg = "err_code:{err_code} err_msg:{err_msg}".format(err_code=err_code,err_msg=err)
    log_debug.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }

# [question_manage]
# excel文件导入试题失败
def error_excel_import_questions_msg(request,msg:str):
    err_code = 7000
    err_msg = "user:{id}:{name} err_code:{err_code} err_msg:{err_msg}".format(id=request.user.id, name=request.user.name, err_code=err_code,err_msg=msg)
    log_debug.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }

# [license]
# license已注册，不得重复使用
def error_license_exists_msg(request,msg:str):
    err_code = 8000
    err_msg = "user:{id}:{name} err_code:{err_code} err_msg:{err_msg}".format(id=request.user.id, name=request.user.name, err_code=err_code,err_msg=msg)
    log_data.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }

# license无效，有效天数是 0 天
def error_license_invalid_msg(request,msg:str):
    err_code = 8001
    err_msg = "user:{id}:{name} err_code:{err_code} err_msg:{err_msg}".format(id=request.user.id, name=request.user.name, err_code=err_code,err_msg=msg)
    log_data.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }

# license过期
def error_license_expired_msg(msg:str):
    err_code = 8002
    err_msg = msg
    # log_data.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }

# [video]
# excel文件导入试题失败
def error_video_upload_is_not_staff_msg(request,msg:str):
    err_code = 9000
    err_msg = "user:{id}:{name} err_code:{err_code} err_msg:{err_msg}".format(id=request.user.id, name=request.user.name, err_code=err_code,err_msg=msg)
    log_debug.error(err_msg)
    return {"err_code": err_code, "msg": err_msg, }



# DRF restful API






