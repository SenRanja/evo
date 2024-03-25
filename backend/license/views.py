# encoding=utf-8

from conf.errors import success_msg, error_license_exists_msg, error_license_invalid_msg
from django.http import JsonResponse as JR
from lib.handle_license_data import check_license_day_num, load_from_data_file, dump_to_data_file, check_license_data_valid

def get_license_days_num(request):
    # if time_unit==None:
    #     time_unit = 'hour'
    license_data_dict = load_from_data_file()
    # 已运行时间
    past_hours = license_data_dict["past_hours_count"]
    # license总时间
    total_hours = 0
    for lid, hours in license_data_dict["licnese"].items():
        total_hours = total_hours + hours
    license_data_dict["total_hours"] = total_hours
    # 剩余时间
    license_data_dict["left_days"] = int((total_hours - past_hours)/24)

    # 查看license是否有文件过期问题
    license_valid_bool, license_valid_reason = check_license_data_valid()
    license_data_dict["license_valid_bool"] = license_valid_bool
    license_data_dict["license_valid_reason"] = license_valid_reason

    return JR(success_msg(license_data_dict))

def submit_license(request, license):
    license_data_dict = load_from_data_file()
    # print(license_data_dict)

    # 检查license是否已使用，若使用则响应失败
    for stored_license in license_data_dict['licnese'].keys():
        if license == stored_license:
            return JR(error_license_exists_msg(request, "license已注册"))

    # 检查license是有效性，若有效则计入 PICKLE_LICENSE_DATA
    day_num = check_license_day_num(license)
    if day_num==0:
        # license无效
        return JR(error_license_invalid_msg(request, "license invalid"))
    else:
        # license有效，存入 PICKLE_LICENSE_DATA
        license_data_dict['licnese'][license] = day_num * 24    # 存入小时数
        # print(license_data_dict)
        dump_to_data_file(license_data_dict)

        return JR(success_msg(day_num))