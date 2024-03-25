# encoding=utf-8
import json
from decimal import Decimal

from conf.errors import success_msg
from django.http import JsonResponse as JR
from exam_manage.models import ExamManage_QuestionDatabase, ExamManage
from exam_score.models import ExamScoreResult, ExamSubjectiveResult
from question_manage.models import ExamQuestion

def handle_objective_questions_calculate(question_type, reference_answer, stu_answer, exam_question_obj, multiple_half_flag) -> bool:
    '''计算客观题成绩，此处仅返回bool，若返回None说明非客观题
    多选题选错全不得分
    客观题题型类型： 判断，单选，多选'''
    if question_type == '判断':
        if reference_answer == stu_answer:
            return True
        else:
            return False
    elif question_type == '单选':
        # 由于学生答案是  "stu_answer": "国土安全部"
        options = exam_question_obj.choice_text.split("|")
        # 根据|切割为 如 {'A': '海莲花', 'B': '人面马', 'C': '方程式', 'D': 'NASA'} 的答案数据
        reference_answer_dict = dict()
        for i, option in enumerate(options):
            reference_answer_dict[chr(65 + i)] = option
        reference_answer_option = reference_answer_dict[reference_answer]
        if reference_answer_option == stu_answer:
            return True
        else:
            return False
    elif question_type == '多选':
        # 目前是选错、少选不得分
        # 由于学生答案是  "stu_answer": ["拦截特定的信令", ...]
        # 建立ABCD索引 得 reference_answer_dict
        options = exam_question_obj.choice_text.split("|")
        reference_answer_dict = dict()
        for i, option in enumerate(options):
            reference_answer_dict[chr(65 + i)] = option

        # 使用 set 判断学生答案是否正确
        reference_answer_set = set()
        for alpha in reference_answer:
            reference_answer_set.add(reference_answer_dict[alpha])

        stu_answer = set(stu_answer)

        if stu_answer == reference_answer_set:
            return True
        else:
            if multiple_half_flag==False:
                return False
            else:
                # 如果多选一半分策略开启，返回 元组 (True, 'half')
                if stu_answer.issubset(reference_answer_set):
                    return (True, 'half')
                else:
                    return False
    else:
        return None

def calculate_score(request, exam_id):
    data = json.loads(request.body)
    score = 0

    user = request.user

    # 获取 exam_manage_id 用于从 考试--题库 题目分值设置 获取该题分值
    EM_obj = ExamManage.objects.get(id=exam_id)

    # multiple_half_flag 标志位
    # false 多选题少选不得分， true少选得一半分数
    multiple_half_flag = EM_obj.multiple_half

    # 如果之前没提交成绩，则新建；若提交，则对本次请求不作任何处理
    double_check = ExamScoreResult.objects.filter(user=user, exam_manage=EM_obj).exists()

    # double_check==False 即 没有 用户--考试场次 的 成绩
    if double_check==False:
        # 客观题 逐题计算分值
        question_list = data
        for single_question in question_list:
            if 'stu_answer' in single_question.keys():
                # exam_question_obj 从题库中找出正确答案，和 学生答卷传入的 stu_answer 进行比较
                exam_question_obj = ExamQuestion.objects.get(id=single_question['id'])
                single_score = handle_objective_questions_calculate(
                    exam_question_obj.question_type,    # 试题类型
                    exam_question_obj.reference_answer, # 参考答案
                    single_question['stu_answer'],      # 学生答案
                    exam_question_obj,                  # 原题，方便部分题目进行校验
                    multiple_half_flag,                 # 传入多选题少选 的得分策略
                )
                if single_score!=None:
                    # 客观题，积分入库
                    # 非None意味着 客观题 ;None意味着非客观题，此处不计算；若返回bool则是本题判分

                    # 获取 exam_manage_id 用于从 考试--题库 题目分值设置 获取该题分值
                    EQ_obj = ExamManage_QuestionDatabase.objects.get(exam_manage=EM_obj,
                             question_type=exam_question_obj.question_type,
                             difficulty_level=exam_question_obj.difficulty_level,
                             question_database=exam_question_obj.question_database
                    )
                    single_item_score_set = EQ_obj.single_question_score

                    if single_score==True:
                        # 计入客观题总分
                        score = score + single_item_score_set
                        # self_item_score是单题得分
                        self_item_score = single_item_score_set
                    elif single_score==(True, 'half'):
                        # 多选题少选得一半分情况
                        # 计入客观题总分
                        score = score + single_item_score_set * Decimal(0.5)
                        # self_item_score是单题得分
                        self_item_score = single_item_score_set * Decimal(0.5)
                    else:
                        self_item_score = 0

                    ExamSubjectiveResult.objects.create(
                        user=user,
                        exam_manage=EM_obj,
                        sub_obj="客观",
                        exam_question=exam_question_obj,
                        stu_answer=single_question['stu_answer'],
                        score=self_item_score,
                    )
                else:
                    # if ExamQuestion.objects.filter(id=single_question['id']).exists(): 其实if处代码已经获取试题本身
                    # 本题是主观题，存入 ExamSubjectiveResult 的 model 表中
                    ExamSubjectiveResult.objects.create(
                        user=user,
                        exam_manage=EM_obj,
                        sub_obj="主观",
                        exam_question=exam_question_obj,
                        stu_answer=single_question['stu_answer'],
                        # score=None, 本处代码仅存储，不对主观题判分
                    )

        # 将客观题分数计算存入数据库
        ESR_obj = ExamScoreResult.objects.create(
            user = user,
            name = user.name,
            stu_id = user.stu_id,
            exam_manage=EM_obj,
            objective_score=score,
            # subjective_score 非此处计算
            score=score,
            sub_block=True,
        )

    return JR(success_msg(score))

def get_sub_without_score(request, exam_id):
    user = request.user
    if exam_id == 0:
        answers = ExamSubjectiveResult.objects.filter(sub_obj="主观", score=None).order_by('exam_question')
    else:
        em = ExamManage.objects.get(id=exam_id)
        answers = ExamSubjectiveResult.objects.filter(sub_obj="主观", score=None, exam_manage=em).order_by('exam_question')
    ret = []
    for a in answers:
        # 获取题设分支
        set_score = ExamManage_QuestionDatabase.objects.get(
            exam_manage=a.exam_manage,
            question_database=a.exam_question.question_database,
            question_type=a.exam_question.question_type,
            difficulty_level=a.exam_question.difficulty_level,
        ).single_question_score
        ret.append({
            'id': a.id,
            'exam_manage': a.exam_manage.id,
            'exam_question': a.exam_question.question_text,
            'question_type': a.exam_question.question_type,
            'stu_answer': a.stu_answer,
            "reference_answer": a.exam_question.reference_answer,
            'set_score': set_score,
        })
    return JR({"data": ret})


def check_idcard_tail(request, id_card):
    "交卷验证身份证后六位"
    user = request.user
    whole_id_card = user.id_card
    tail_of_whole_id_card = whole_id_card[-6:]
    flag = False
    if id_card==tail_of_whole_id_card:
        flag = True
    return JR({"data": flag})

def submit_sub_score(request):
    data = json.loads(request.body)
    # user = request.user
    # print(data)
    # 循环遍历传入list，如果老师判分，则有score字段，没有判分的只有set_score字段
    for item in data:
        # 主观题记分，保存老师判分
        if item.get('score')!=None:
            esr = ExamSubjectiveResult.objects.get(id=item['id'])
            esr.score = item['score']
            esr.save()
        # 对当前判卷 重新计分
        if item.get('score') != None:
            # 成绩单总分、主观题总分计分

            # 如果用户已经有 总分成绩单（客观题计分默认出的成绩单）
            esr = ExamSubjectiveResult.objects.get(id=item['id'])
            if ExamScoreResult.objects.filter(exam_manage=esr.exam_manage, user=esr.user).exists():
                exam_score = ExamScoreResult.objects.get(exam_manage=esr.exam_manage, user=esr.user)
                # sub_results 主观题成绩 重新计分
                sub_results_score = 0
                sub_results = ExamSubjectiveResult.objects.filter(exam_manage=esr.exam_manage, user=esr.user, sub_obj="主观")
                for s in sub_results:
                    if s.score!=None:
                        sub_results_score = sub_results_score + s.score
                # 存储入成绩单，总分、主观题分
                exam_score.subjective_score = sub_results_score
                exam_score.score = exam_score.objective_score + sub_results_score
                exam_score.save()
            # 纯主观题，无客观题
            else:
                # 无客观题的  总分成绩单， 第一次将主观题分数计算总成绩，存入数据库
                stu_user = esr.user
                exam_manage_obj = esr.exam_manage
                ESR_obj = ExamScoreResult.objects.create(
                    user=stu_user,
                    name=stu_user.name,
                    stu_id=stu_user.stu_id,
                    exam_manage=exam_manage_obj,
                    objective_score=0,    # 纯主观题第一次没见客观计分，此处设None
                    subjective_score=item.get('score'),
                    score=item.get('score'),
                    sub_block=True,
                )
    return JR({"data": data})