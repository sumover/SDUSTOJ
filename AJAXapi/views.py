import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from OnlineJudge.models import *


def contestStaticReload(request, course_id):
    course = Course.objects.get(pk=course_id)
    statusmap = {}
    for contest in course.contest_set.all():
        statusmap[contest.id] = contest.nowContestStatus()
    return HttpResponse(json.dumps(statusmap), content_type='application/json')
