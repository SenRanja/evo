# encoding=utf-8
from exam_score.models import ExamScoreResult, ExamSubjectiveResult
from exam_manage.models import ExamManage
from rest_framework import viewsets, filters
from exam_score.serializer import ExamScoreResultSerializer, ExamSubjectiveResultSerializer
from rest_framework.response import Response


class ExamScoreResultViewSet(viewsets.ModelViewSet):
    """考试成绩管理"""

    queryset = ExamScoreResult.objects.all().order_by('-exam_manage')
    serializer_class = ExamScoreResultSerializer

    filter_backends = [filters.SearchFilter, ]
    # exam_manage 是一个外键，在其 exam_name 字段上执行搜索，使用双下划线连接
    search_fields = ['name', 'stu_id', 'exam_manage__exam_name']

    def list(self, request, *args, **kwargs):
        # 根据访问者是 admin stu tea 返回不同内容
        # 自定义搜索返回数据
        user = request.user
        if user.role == "admin" or user.role == "tea":
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.queryset.filter(user=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            # 使其返回 考试id 为 考试名字
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                em = ExamManage.objects.get(id=item['exam_manage'])
                item['exam_manage'] = em.exam_name
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ExamSubjectiveResultViewSet(viewsets.ModelViewSet):
    """考试成绩主观题管理"""

    queryset = ExamSubjectiveResult.objects.all().order_by('exam_question')
    serializer_class = ExamSubjectiveResultSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


