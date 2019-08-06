from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from .models import *


def checkWhetherLogin(func):
    def view(request, *args, **kwargs):
        if request.session.get('loginUserId', False):
            return HttpResponseRedirect(reverse('login'))
        else:
            return func(request, *args, **kwargs)

    return view


def checkWhetherContestExist(func):
    def view(request, contest_id, *args, **kwargs):
        try:
            Contest.objects.get(pk=contest_id)
        except Contest.DoesNotExist:
            return render(request, '', {
                'contestNotExist': True,
            })
        else:
            return func(request, contest_id, *args, **kwargs)

    return view


"""
1. 权限问题
    通常来讲, Administrator 可以查看任意界面, 所以这里的问题只有Student
    对于Course, Contest, Problem, 我们需要检测一下Student是否被允许查看, 而且, 他们是迭代的.
    如果没有权限, 则跳转至index, 如果有就不管了
    就酱.
    逻辑有点迷, 等写完再说
"""


def checkUserLogin(func):
    def view(request, *args, **kwargs):
        try:
            request.session['loginUserId']
        except KeyError:
            return HttpResponseRedirect('/OnlineJudge/')
        else:
            return func(request, *args, **kwargs)

    return view


def addHeaderContext(func):
    """
    TODO the func must have this argument: request, context
    to save code to check some parameter to header.html template, we use this to construct a context
    :param func: the function to be decreator
    :return: ...~23333
    """

    def view(request, *args, **kwargs):
        context = {}
        userid = request.session.get('loginUserId', -1)
        if userid != -1:  # user not login
            context['userNotLogin'] = False
            try:  # check whether user exist, for code strong.
                context['userPermission'] = User.objects.get(pk=userid).transferType().getPermission()
            except User.DoesNotExist:  # as we know, this check not very important
                context['userNotExist'] = True
            else:  # so we add username and userNotExist = False into template
                context['user'] = User.objects.get(pk=userid)
                context['userNotExist'] = False
        else:  # if user not login, mark userNotLogin is True
            context['userNotLogin'] = True

        return func(request, context, *args, **kwargs)

    return view


###########################################

@addHeaderContext
def index(request, context):
    return render(request, 'OnlineJudge/index.html', context)


@addHeaderContext
def toLoginPage(request, context):
    if context['userNotLogin']:
        return render(request, 'OnlineJudge/login.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))


def loginParameterChecker(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return render(request, 'OnlineJudge/login.html', {
            'userNotExist': True
        })
    else:
        request.session['loginUserId'] = user.pk
        return HttpResponseRedirect("/OnlineJudge/")


@checkWhetherLogin
def logout(request):
    del request.session['loginUserId']
    return HttpResponseRedirect('/OnlineJudge/')


@checkWhetherLogin
@addHeaderContext
def userCourse(request, context):
    student = User.objects.get(pk=request.session['loginUserId']).transferType()
    context['courses'] = student.course_set.all()
    return render(request, '', context)


@checkWhetherLogin
@addHeaderContext
def courseDetail(request, context, course_id):
    student = User.objects.get(pk=request.session['loginUserId']).transferType()
    context['contests'] = student.course_set.get(pk=course_id)
    return render(request, '', context)


@checkWhetherLogin
@addHeaderContext
def contestDetail(request, context, course_id, contest_id):
    context['contestProblems'] = Contest.objects.get(contest_id)
    return render(request, '', context)


@checkWhetherLogin
@addHeaderContext
def problemDetail(request, context, course_id, contest_id, problem_id):
    context['problem'] = Problem.objects.get(pk=problem_id)
    return render(request, '', context)


def submit(request, contest_id, problem_id):
    source = request.POST['sources']
    lang = request.POST['language']
    submitStudent = User.objects.get(pk=request.session.get('loginUserId')).transferType()
    submission = Submission(
        submittime=Contest.getNowUNIXTimeStamp(),
        submitfile=source,
        prob=Problem.objects.get(pk=problem_id),
        lang=lang,
        submitStudent=submitStudent
    )
    submission.save()
    status = SubmissionStatus(aimSubmission=submission, staus=-1)
    status.save()
    return HttpResponseRedirect(reverse(''))


@checkWhetherLogin
@addHeaderContext
def contestProblemStatus(request, context, contest_id):
    user = User.objects.get(pk=request.session.get('loginUserId')).transferType()
    if user.getPermission() > 10:
        context['submitStatus'] = [
            status for status in SubmissionStatus.objects.all()
            if (status.aimSubmission.submitStudent.id == user.id) and
               (status.aimSubmission.submitContest.id == contest_id)
        ]
        pass
    else:
        context['submitStatus'] = [
            status for status in SubmissionStatus.objects.all()
            if status.aimSubmission.submitContest.id == contest_id
        ]
        pass
    return render(request, '', context)
