# encoding=utf-8

import json
from datetime import datetime
from random import sample

from conf.errors import success_msg
from django.contrib.auth.models import Group
from django.http import JsonResponse as JR
from django.utils import timezone
from exam_manage.models import ExamManageClass, ExamManage, ExamManage_QuestionDatabase
from exam_score.models import ExamScoreResult, ExamSubjectiveResult
from question_manage.models import ExamQuestion

from lib.timeFormat import format_date
# 导入word文档生成docx格式文件
from exam_manage.docx_gen import genDocx

def sortByQuestionType(data:list):
    # 定义排序顺序
    type_order = ["单选", "多选", "判断", "填空", "简答", "论述"]
    # 根据排序顺序对题目列表进行排序
    sorted_questions = sorted(data, key=lambda x: type_order.index(x["question_type"]))
    # 输出排序后的结果
    ret = []
    for question in sorted_questions:
        ret.append(question)
    return ret


def add_class_exam_manage(request):
    '''考试场次(exam) 与参加本次考试的 班级（group）'''
    data = json.loads(request.body)

    group_class_name = data["group_class"]
    group = Group.objects.get(name=group_class_name)
    exam_manage_pk = data['exam_manage_pk']
    exam_manage_obj = ExamManage.objects.get(id=exam_manage_pk)

    ExamManageClass.objects.create(group_class=group, exam_manage_pk=exam_manage_obj)

    return JR(success_msg("okok"))

def add_question_database_exam_manage(request):
    '''增加 考试--题库 对应'''
    data = json.loads(request.body)
    return JR(success_msg("okok"))

def get_exam_manages(request):
    '''根据用户自己所在班级(group) 获取 考试场次'''
    user = request.user
    if user.role == "stu":
        ret = []
        groups = user.groups.all()
        for single_group in groups:
            emc_list = ExamManageClass.objects.filter(group_class=single_group)
            for single_exam in emc_list:
                # exam_manage_pk是外键，因此 single_exam_obj 是 ExamManage 的实例化对象
                single_exam_obj = single_exam.exam_manage_pk
                if single_exam_obj.is_archived==False:
                    # 只返回未归档状态的考试

                    # 获取当前时间
                    current_time = timezone.now()
                    # 根据当前时间，设置考试状态
                    if single_exam_obj.start_time <= current_time <= single_exam_obj.end_time:
                        exam_status = "doing"
                    elif current_time < single_exam_obj.start_time:
                        exam_status = "to do"
                    elif current_time > single_exam_obj.end_time:
                        exam_status = "done"

                    ret.append({
                        'id': single_exam_obj.id,
                        'exam_name': single_exam_obj.exam_name,
                        'exam_type': single_exam_obj.exam_type,
                        'start_time': format_date(str(single_exam_obj.start_time)),
                        'end_time': format_date(str(single_exam_obj.end_time)),
                        'duration': single_exam_obj.duration,
                        'max_score': single_exam_obj.max_score,
                        'is_archived': single_exam_obj.is_archived,
                        "exam_status": exam_status
                    })
        return JR({'data': ret})
    # elif user.role == "tea":
    else:
        emc_list = ExamManage.objects.filter(is_archived=False)
        ret = []
        for single_exam in emc_list:
            # 获取当前时间
            current_time = timezone.now()
            # 根据当前时间，设置考试状态
            if single_exam.start_time <= current_time <= single_exam.end_time:
                exam_status = "doing"
            elif current_time < single_exam.start_time:
                exam_status = "to do"
            elif current_time > single_exam.end_time:
                exam_status = "done"
            ret.append({
                'id': single_exam.id,
                'exam_name': single_exam.exam_name,
                'exam_type': single_exam.exam_type,
                'start_time': format_date(str(single_exam.start_time)),
                'end_time': format_date(str(single_exam.end_time)),
                'duration': single_exam.duration,
                'max_score': single_exam.max_score,
                'is_archived': single_exam.is_archived,
                "exam_status": exam_status
            })
        return JR({'data': ret})


def detect_examed(request, exam_id):
    "检查用户是否参加过这次考试"
    user = request.user
    EM_obj = ExamManage.objects.get(id=exam_id)
    double_check = ExamScoreResult.objects.filter(user=user, exam_manage=EM_obj).exists()
    ret = {
        'double_check': double_check,
        'exam_type': EM_obj.exam_type
    }
    return JR(ret)

def get_old_results(request, exam_id):
    "返回已提交的旧卷"
    user = request.user
    ret = []
    EM_obj = ExamManage.objects.get(id=exam_id)
    results = ExamSubjectiveResult.objects.filter(user=user, exam_manage=EM_obj)
    for result in results:
        ret.append({
            'sub_obj': result.sub_obj,
            'exam_question': result.exam_question.question_text,
            'reference_answer': result.exam_question.reference_answer,
            'choice_text': result.exam_question.choice_text,
            'stu_answer': result.stu_answer,
            'score': result.score,
        })
    return JR({'data':ret})

def get_exam_paper(request, exam_id):
    """获取考试试题，试题根据题库随机生成，顺序打乱
    返回格式json
    如 {"data":
        [
            {
                ""
            },
        ]
    }
    """
    data = []
    exam_manage = ExamManage.objects.get(id=exam_id)
    for single_question_type in ExamManage_QuestionDatabase.objects.filter(exam_manage=exam_manage):
        # N 是考试期望该类型题目的 个数
        N = single_question_type.question_num
        # 考试期望该题型 单个/分值
        single_score = single_question_type.single_question_score
        # 根据 难易程度  题目类型  题库 选出全部符合要求的试题 questions
        questions = ExamQuestion.objects.filter(
            question_database=single_question_type.question_database,
            question_type=single_question_type.question_type,
            difficulty_level=single_question_type.difficulty_level,
        )
        # random.sample 不重复的从 迭代对象 选中 制定个数 的列表，会自行打乱数据，和原序列顺序无关
        random_questions = sample(list(questions), min(N, len(questions)))
        for single_question in random_questions:
            item = {
                    'id': single_question.id,
                    'question_type': single_question.question_type,
                    # 'reference_answer': single_question.reference_answer,
                    'question_name': single_question.question_name,
                    'question_text': single_question.question_text,
                    'choice_text': single_question.choice_text,
                    'question_image_data': single_question.question_image_data,
                    'difficulty_level': single_question.difficulty_level,
                    'description': single_question.description,
                    'subject': single_question.subject.subject,
                    'question_database': single_question.question_database,
                    'author': single_question.author,
                    'score': single_score,
                }
            if exam_manage.exam_type == '模拟':
                # 只有考试是 模拟 状态，才会返回答案
                item['reference_answer'] = single_question.reference_answer
            data.append(item)
    sorted_data = sortByQuestionType(data)
    ret_json = {
        'question_list': sorted_data    # list，是试题列表
    }
    return JR(ret_json)

def generate_exam_paper_word(request, exam_id):
    """获取考试试题，试题根据题库随机生成，顺序打乱
    返回格式json
    如 {"data":
        [
            {
                ""
            },
        ]
    }
    """
    data = []
    exam_manage = ExamManage.objects.get(id=exam_id)
    for single_question_type in ExamManage_QuestionDatabase.objects.filter(exam_manage=exam_manage):
        # N 是考试期望该类型题目的 个数
        N = single_question_type.question_num
        # 考试期望该题型 单个/分值
        single_score = single_question_type.single_question_score
        # 根据 难易程度  题目类型  题库 选出全部符合要求的试题 questions
        questions = ExamQuestion.objects.filter(
            question_database=single_question_type.question_database,
            question_type=single_question_type.question_type,
            difficulty_level=single_question_type.difficulty_level,
        )
        # random.sample 不重复的从 迭代对象 选中 制定个数 的列表，会自行打乱数据，和原序列顺序无关
        random_questions = sample(list(questions), min(N, len(questions)))
        for single_question in random_questions:
            item = {
                    'id': single_question.id,
                    'question_type': single_question.question_type,
                    # 'reference_answer': single_question.reference_answer,
                    'question_name': single_question.question_name,
                    'question_text': single_question.question_text,
                    'choice_text': single_question.choice_text,
                    'question_image_data': single_question.question_image_data,
                    'difficulty_level': single_question.difficulty_level,
                    'description': single_question.description,
                    'subject': single_question.subject.subject,
                    'question_database': single_question.question_database,
                    'author': single_question.author,
                    'score': single_score,
                }
            if exam_manage.exam_type == '模拟':
                # 只有考试是 模拟 状态，才会返回答案
                item['reference_answer'] = single_question.reference_answer
            data.append(item)
    sorted_data = sortByQuestionType(data)
    # data 是本场考试全部题的list
    # 传入genDocx生成word格式考题
    ret_filename = genDocx(sorted_data, exam_manage)
    return JR({
        'data': 'http://shenyanjian.cn/static/media/documents/'+ret_filename,
        'filename': ret_filename,
    })