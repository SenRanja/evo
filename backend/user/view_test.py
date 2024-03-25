# encoding=utf-8
# 测试API
import json

from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse as JR
from guardian.decorators import permission_required

from guardian.shortcuts import assign_perm, remove_perm, get_perms, get_users_with_perms

from conf.errors import success_msg, error_duplicate_group_add_msg
from user.models import User
from video.models import Video
from module.models import Module


def test_1(request):
    rsp = json.loads("""
    {
    "msg": "ok",
    "data": {
        "id": 3,
        "username": "admin",
        "avatar": "https://www.nuc.edu.cn/images/nuc2018_08.png",
        "super": 1,
        "role": {
            "id": 2,
            "name": "超级管理员"
        },
        "menus": [
            {
                "id": 5,
                "rule_id": 0,
                "status": 1,
                "create_time": "2019-08-11 13:36:09",
                "update_time": "2021-12-21 19:31:11",
                "name": "后台面板",
                "desc": "index",
                "frontpath": null,
                "condition": null,
                "menu": 1,
                "order": 1,
                "icon": "help",
                "method": "GET",
                "child": [
                    {
                        "id": 10,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "主控台11",
                        "desc": "index",
                        "frontpath": "/",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    },
                    {
                        "id": 10,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "主控台12",
                        "desc": "index",
                        "frontpath": "/",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    }
                ]
            },
            {
                "id": 6,
                "rule_id": 0,
                "status": 1,
                "create_time": "2019-08-11 13:36:09",
                "update_time": "2021-12-21 19:31:11",
                "name": "考试管理",
                "desc": "index",
                "frontpath": null,
                "condition": null,
                "menu": 1,
                "order": 1,
                "icon": "help",
                "method": "GET",
                "child": [
                    {
                        "id": 10,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "试题列表",
                        "desc": "index",
                        "frontpath": "/questions/list",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    },
                    {
                        "id": 10,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "分类列表",
                        "desc": "index",
                        "frontpath": "/category/list",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    },
                    {
                        "id": 10,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "考试状态",
                        "desc": "index",
                        "frontpath": "/exam_questions/examing",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    },
                    {
                        "id": 11,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "用户列表",
                        "desc": "index",
                        "frontpath": "/user/list",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    },
                    {
                        "id": 12,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "公告列表",
                        "desc": "index",
                        "frontpath": "/notice/list",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    }
                ]
            },
            {
                "id": 7,
                "rule_id": 0,
                "status": 1,
                "create_time": "2019-08-11 13:36:09",
                "update_time": "2021-12-21 19:31:11",
                "name": "学习管理",
                "desc": "index",
                "frontpath": null,
                "condition": null,
                "menu": 1,
                "order": 1,
                "icon": "help",
                "method": "GET",
                "child": [
                    {
                        "id": 10,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "视频学习",
                        "desc": "index",
                        "frontpath": "/video_study/list",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    }
                ]
            },
            {
                "id": 8,
                "rule_id": 0,
                "status": 1,
                "create_time": "2019-08-11 13:36:09",
                "update_time": "2021-12-21 19:31:11",
                "name": "系统管理",
                "desc": "index",
                "frontpath": null,
                "condition": null,
                "menu": 1,
                "order": 1,
                "icon": "help",
                "method": "GET",
                "child": [
                    {
                        "id": 12,
                        "rule_id": 5,
                        "status": 1,
                        "create_time": "2019-08-11 13:37:02",
                        "update_time": "2021-12-21 20:21:23",
                        "name": "配置",
                        "desc": "index",
                        "frontpath": "/setting/base",
                        "condition": null,
                        "menu": 1,
                        "order": 20,
                        "icon": "home-filled",
                        "method": "GET",
                        "child": []
                    }
                ]
            }
        ],
        "ruleNames": [
            "createRule,POST",
            "getStatistics3,GET",
            "getStatistics1,GET"
        ]
    }
}

    """)
    return JR(rsp)


def test_2(request):
    rsp = json.loads("""{
    "msg": "ok",
    "data": {
        "panels": [
            {
                "title": "支付订单",
                "value": 51,
                "unit": "年",
                "unitColor": "success",
                "subTitle": "总支付订单",
                "subValue": 51,
                "subUnit": ""
            },
            {
                "title": "订单量",
                "value": 555,
                "unit": "周",
                "unitColor": "danger",
                "subTitle": "转化率",
                "subValue": "60%",
                "subUnit": ""
            },
            {
                "title": "销售额",
                "value": 3.74,
                "unit": "年",
                "unitColor": "",
                "subTitle": "总销售额",
                "subValue": 3.74,
                "subUnit": ""
            },
            {
                "title": "新增用户",
                "value": 16,
                "unit": "年",
                "unitColor": "warning",
                "subTitle": "总用户",
                "subValue": 16,
                "subUnit": "人"
            }
        ]
    },
    "path": "观看完整课程地址：https://study.163.com/course/courseMain.htm?courseId=1212775807&share=2&shareId=480000001892585"
}""")
    return JR(rsp)


def test_3(request):
    rsp = json.loads("""{
    "msg": "ok",
    "data": {
        "x": [
            "00",
            "23",
            "22",
            "21",
            "20",
            "19",
            "18",
            "17",
            "16",
            "15",
            "14",
            "13",
            "12",
            "11",
            "10",
            "09",
            "08",
            "07",
            "06",
            "05",
            "04",
            "03",
            "02",
            "01"
        ],
        "y": [
            0,
            0,
            0,
            0,
            0,
            4,
            6,
            3,
            0,
            6,
            3,
            0,
            0,
            11,
            18,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]
    },
    "path": "观看完整课程地址：https://study.163.com/course/courseMain.htm?courseId=1212775807&share=2&shareId=480000001892585"
}
    """)
    return JR(rsp)


def test_4(request):
    rsp = json.loads("""{
    "msg": "ok",
    "data": {
        "goods": [
            {
                "label": "审核中",
                "value": 27
            },
            {
                "label": "销售中",
                "value": 36
            },
            {
                "label": "已下架",
                "value": 85
            },
            {
                "label": "库存预警",
                "value": 29
            }
        ],
        "order": [
            {
                "label": "待付款",
                "value": 171
            },
            {
                "label": "待发货",
                "value": 16
            },
            {
                "label": "已发货",
                "value": 1
            },
            {
                "label": "退款中",
                "value": 17
            }
        ]
    },
    "path": "观看完整课程地址：https://study.163.com/course/courseMain.htm?courseId=1212775807&share=2&shareId=480000001892585"
}""")
    return JR(rsp)


def group_add(request, group_name):
    try:
        group = Group.objects.create(name=group_name)
        group.save()
    except Exception as err:
        user_id = str(request.user.id)
        username = request.user.name
        if 'Duplicate entry' in str(err):
            return JR(error_duplicate_group_add_msg(user_id + username + str(err)))
    return JR(success_msg('new group add successfully'))


def group_delete(request, group_name):
    # try:
    # group = Group.objects.filter(name=group_name).first()
    group = Group.objects.get(name=group_name)
    group.delete()
    return JR(success_msg('group del successfully'))


# 用户退出所有用户组user.groups.clear()
# 用户组中所有用户退出组group.user_set.clear()
def group_add_user(request, group_name):
    # user.groups.add(group)或group.user_set.add(user)
    # User.objects.get(username='test@ops-coffee.cn').groups.add(group)
    pass


def group_remove_user(request, group_name):
    # user.groups.remove(group)或group.user_set.remove(user)
    pass


def user_has_perm(request):
    '''Django的auth系统提供了APP(参考settings的INSTALLED_APPS)的权限控制， 即可以检查用户是否对某个数据表拥有增(add), 改(change), 删(delete)权限(django默认的权限机制，的最小颗粒度是 表)。

    auth系统无法提供对象级的权限控制， 即检查用户是否对数据表中某条记录拥有增改删的权限。如果需要对象级权限控制可以使用django-guardian.

    permission = Permission.objects.get(codename='access_log')
    groups.permissions.add(permission)
    '''
    # user.groups.remove(group)或group.user_set.remove(user)
    # User.user_permissions.add('blog.add_users')
    # print("获取用户权限")
    # # get_user_permissions()仅包含用户直接被分配的权限，不包括通过组间接分配的权限
    # s = request.user.get_user_permissions()
    # print(s)
    # print("获取全部权限")
    # # get_all_permissions()用户拥有的所有权限集合，包括直接和通过组间接分配的权限
    # s = request.user.get_all_permissions()
    # print(s)

    # video = Video.objects.get(name='fsfsasfffffde')
    user = request.user
    print("当前用户 "+user.name)
    # 查验权限
    # res = user.has_perm('video.delete_video', video)
    # res = user.has_perm('video.custom_add_video', video)
    # print(res)
    # 删除权限
    # 不可以一次操作多个用户（推荐循环处理），如果无第三参数，则是删除整个model的权限
    # res = remove_perm('video.custom_add_video',user, video)
    # print(res)
    # 赋予权限
    # 可以给多个用户赋予权限，如 assign_perm('engine.commontask_run', User.objects.filter(id__in=[3,4]), task)
    # print(assign_perm('video.delete_video', user, video))
    # 查验权限
    pm = 'video.change_video'
    video = Video.objects.get(id=32)
    print(user.has_perm(pm, video))
    print(assign_perm(pm, user))
    print(assign_perm(pm, user, video))
    # print(assign_perm(pm, user)) # 不写 目标obj 则是对表进行操作
    print(user.has_perm(pm, video))
    # 根据用户和对象获取权限
    # res = get_perms(user, video)
    # print(res)
    # 获取目标对象的所有涉及权限的用户对象（默认不含superuser），with_superusers=True 表示查看包括超级用户
    # res = get_users_with_perms(video, with_superusers=True)
    # print(res)
    # 如果我们想要查看用户具有的权限，可以设置参数attach_perms = True，返回的结构是以用户为key权限为value的一个字典，看起来清晰明了
    # get_users_with_perms(task, with_superusers=True, attach_perms=True)
    # 仅想查看具有某个权限的用户，可以设置only_with_perms_in参数，例如我们只想查看对象所有具有commontask_change权限的用户
    # get_users_with_perms(task, with_superusers=True, only_with_perms_in=['commontask_change'])
    # 默认情况下用户所属组如果具有权限的话也会返回，例如上边的我们把用户test加入到了group，然后给group赋予了权限，那么用户也就具有了相应的权限，如果我们只想查看直接赋予用户的权限，而并非间接通过group取得的权限用户列表，我们可以设置参数with_group_users = False，此参数默认为True
    # get_users_with_perms(task, with_superusers=True, with_group_users=False)
    # 与get_users_with_perms方法相类似的是get_groups_with_perms方法，但get_groups_with_perms要简单许多，只能接收两个参数object和attach_perms
    # 根据 用户 和 权限 来获取对象列表
    # get_objects_for_user(user, 'engine.commontask_run')
    # get_objects_for_user(user, ['engine.commontask_run', 'engine.commontask_change'])
    # 仅满足列表中的任意一个权限，可以添加第三个参数any_perm=True
    # get_objects_for_user(user, ['engine.commontask_run', 'engine.commontask_change'], any_perm=True)

    return JR(success_msg('successfully'))


def add_video(request, video_name):
    Video.objects.create(name=video_name)
    return JR(success_msg('successfully'))

# 如下，from guardian.decorators import permission_required也对django默认的permission_required装饰器，根据django默认的表为最小颗粒度鉴权的 用户是否具有整个model的commontask_change权限
# @permission_required('engine.commontask_change')
# 如下，'video_name'是形参， 'name'是数据库中字段名，这是用户对象到对象具有权限才会触发的删除动作
@permission_required('video.delete_video', (Video, 'name', 'video_name'), return_404=True)
def del_video(request, video_name):
    try:
        _data = Video.objects.get(name=video_name)
        _data.delete()
        return JR({'state': 1, 'message': '删除成功!'})
    except Exception as e:
        return JR({'state': 0, 'message': 'Error: ' + str(e)})

def grp_assign_module(request):
    user = request.user
    print("当前用户", user.name)
    pm = 'module.can_get'
    grp_obj = Group.objects.get(id=1)
    # assign_perm(pm, grp_obj, )
    # remove_perm(pm, user, )

    # 给某group赋予权限，其组内用户也可以访问到该菜单
    # modules = Module.objects.get(id=5)
    # grp_obj = Group.objects.get(id=1)
    # assign_perm(pm, grp_obj, modules)

    module_obj = Module.objects.get(id=2)
    print("应用级权限", user.has_perm(pm))
    print("对象级权限", user.has_perm(pm, module_obj))
    return JR(success_msg("oko"))
