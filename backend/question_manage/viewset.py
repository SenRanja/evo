# encoding=utf-8
from django.contrib.auth.models import Group
from question_manage.models import ExamQuestion
from rest_framework import viewsets, filters
from question_manage.serializer import ExamQuestionSerializer

# DRF要求建立ViewSet

class ExamQuestionViewSet(viewsets.ModelViewSet):
    """试题管理  由于涉及 model的图片以二进制方式存储，无法json传输，因此试题管理的DRF API部分弃用。
    试题管理的DRF API仅用作参考，无实际用途"""
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer

    filter_backends = [filters.SearchFilter, ]
    search_fields = ['question_name', 'question_text', 'description', 'question_database', 'author',]
    # search_fields = ['=question_database', ]
    # 默认情况下，SearchFilter类搜索将使用不区分大小写的部分匹配(icontains)。你可以在search_fields中添加各种字符来指定匹配方法。
    # '^'开始 - 搜索。
    # '='完全匹配。
    # '@'全文搜索。
    # '$'正则表达式搜索。
    # 例如：search_fields = ('=title', )精确匹配title。
    # 前面我们详细介绍了对结果进行过滤的3种方法，接下来我们再看看如何对结果进行排序，这里主要通过DRF自带的OrderingFilter类实现。


