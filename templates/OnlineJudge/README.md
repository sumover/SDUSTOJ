# 1. AJAX of contests.html

AJAX请求:

1.  url:OnlineJudge/api/<int:course_id>/course/

2.  method:get


{
    contestStatuses : {
        contest_id : contestStatus,
        ...
    },
}

exp:
{
    contestStatuses : {
        1 : -1,
        2 : 0,
    },
}

