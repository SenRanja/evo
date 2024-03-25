# encoding=utf-8

from conf.errors import success_msg
from django.http import JsonResponse as JR

from subject_manage.models import Subject, SubjectClass


def get_subject_list(request):
    user = request.user
    ret = []
    ss = Subject.objects.all()
    for s in ss:
        cls = []
        scs = SubjectClass.objects.filter(subject=s)
        for sc in scs:
            cls.append(sc.group.name
                # {
                #     'group_id': sc.group.id,
                #     'group_name': sc.group.name,
                # }
            )
        ret.append({
            'id': s.id,
            'subject': s.subject,
            'creation_time': s.creation_time,
            'description': s.description,
            'groups': cls,
        })
    return JR(success_msg({"data": ret}))