import datetime
import decimal
import time

from django.db import models


# Create your models here.
class Organization(models.Model):
    orgName = models.CharField(max_length=100)
    shortName = models.CharField(max_length=20)


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    create_date = models.DateField(auto_now_add=True)

    def getPermission(self):
        return 0

    def __str__(self):
        return "%s : %s" % (self.pk, self.username)

    def transferType(self):
        try:
            return Student.objects.get(pk=self.id)
        except Student.DoesNotExist:
            try:
                return OrganizationAdministrator.objects.get(pk=self.id)
            except OrganizationAdministrator.DoesNotExist:
                try:
                    return GeneralAdministrator.objects.get(pk=self.id)
                except GeneralAdministrator.DoesNotExist:
                    return SuperAdministrator.objects.get(pk=self.id)


class Student(User):
    nickname = models.CharField(max_length=20)
    creator = models.ForeignKey(to='Administrator', on_delete=models.DO_NOTHING)

    def checkWhetherStudentInSquad(self, squad):
        if isinstance(squad, Squad):
            return self in squad.students
        else:
            return False

    def getPermission(self):
        return 100000


class UserRole(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class Administrator(User):
    role = models.ForeignKey(to='UserRole', on_delete=models.DO_NOTHING)


class OrganizationAdministrator(Administrator):
    def getPermission(self):
        return 1


class SuperAdministrator(Administrator):
    def getPermission(self):
        return 0


class GeneralAdministrator(Administrator):
    subOrganization = models.ForeignKey(to='Organization', on_delete=models.CASCADE)

    def getPermission(self):
        return 2


class Matter(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)


class Squad(Matter):
    squadName = models.CharField(max_length=100)
    students = models.ManyToManyField(to='Student')
    courses = models.ManyToManyField(to='Course')
    subOrg = models.ForeignKey(to='Organization', on_delete=models.CASCADE)

    def checkStudentInSquad(self, student):
        if isinstance(student, Student):
            return student in self.students
        else:
            return False


class Language(models.Model):
    lang = models.CharField(max_length=20)


class Submission(models.Model):
    submittime = models.DecimalField(max_digits=32, decimal_places=9)
    submitfile = models.BinaryField(max_length=128 * 1024)
    prob = models.ForeignKey(to='Problem', on_delete=models.DO_NOTHING)
    lang = models.OneToOneField(to='Language', on_delete=models.DO_NOTHING)
    submitStudent = models.ForeignKey(to='Student', on_delete=models.DO_NOTHING)


class TestCase(models.Model):
    testInput = models.BinaryField(max_length=128 * 1024)
    testOutput = models.BinaryField(max_length=128 * 1024)
    onshow = models.BooleanField(default=False)
    md5input = models.CharField(max_length=100)
    md5output = models.CharField(max_length=100)


class ContestConfig(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    configRole = models.TextField(max_length=1000)


class Course(models.Model):
    creator = models.ForeignKey(Administrator, on_delete=models.DO_NOTHING)
    courseName = models.CharField(max_length=20)
    beginDate = models.DateField()
    endDate = models.DateField()

    def checkStudentParticipateCourse(self, student):
        if isinstance(student, Student):
            squads = self.squad_set
            for squad in squads:
                if student.checkWhetherStudentInSquad(squad):
                    return True
            return False
        else:
            return False


class Contest(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    beginTime = models.DecimalField(max_digits=32, decimal_places=9)
    endTime = models.DecimalField(max_digits=32, decimal_places=9)
    contestproblems = models.ManyToManyField(to='Problem')
    config = models.ForeignKey(ContestConfig, on_delete=models.DO_NOTHING)
    participateCourse = models.ManyToManyField(Course)

    def getContestProblems(self):
        problems = self.contestproblems.all()
        return problems

    def checkWhetherNowContestStatus(self):
        now = time.time()
        if now < self.beginTime:
            return -1
        elif now > self.endTime:
            return 1
        else:
            return 0

    def canSubmit(self) -> bool:
        return self.beginTime < time.time() < self.endTime

    def userCanViewContestDetails(self, user) -> bool:
        if isinstance(user, Administrator):
            return True
        elif isinstance(user, Student):
            squad = user.squad_set[0]
            for course in squad.courses:
                if self in course.contest_set:
                    return True
            return False
        else:
            return False

    @staticmethod
    def getUNIXTimeStampFromDateTime(transferTime) -> decimal:
        if isinstance(transferTime, datetime.datetime):
            return time.mktime(transferTime.timetuple())

    @staticmethod
    def getDateTimeFromUNIXTimeStamp(transferTime) -> datetime:
        if isinstance(transferTime, float):
            return datetime.datetime.fromtimestamp(transferTime)
        else:
            return datetime.datetime.fromtimestamp(float(transferTime))


class SubmissionStatus(Matter):
    aimSubmission = models.OneToOneField(to='Submission', on_delete=models.CASCADE)
    status = models.IntegerField()  # -1 ,0 ,1
    result = models.CharField(max_length=20, blank=True)
    judgingMessage = models.CharField(max_length=10000, blank=True)

    def getStatus(self) -> str:
        return 'PENDING' if self.status == -1 else 'Judging' if self.status == 0 else self.result


class Problem(models.Model):
    creator = models.ForeignKey(Administrator, on_delete=models.DO_NOTHING)
    createTime = models.DateTimeField(auto_now_add=True)
    problemName = models.CharField(max_length=100)
    shortName = models.CharField(max_length=100)
    problemDetail = models.BinaryField(max_length=10 * 1024 * 1024)
    testCases = models.ManyToManyField(to="TestCase")
    problemTags = models.ManyToManyField(to='Tag')

    def __hash__(self):
        return self.id


class Tag(models.Model):
    creator = models.ForeignKey(Administrator, on_delete=models.DO_NOTHING)
    tagRole = models.CharField(max_length=100)

    @staticmethod
    def selectAllProblemByTag(tags):
        allproblem = Problem.objects.all()
        if isinstance(tags, Tag):
            selectProblem = [problem for problem in allproblem if tags in problem.problemTags.all()]
            return selectProblem
        elif isinstance(tags, list):
            selectProblem = set()
            for tag in tags:
                for problem in allproblem:
                    if tag in problem.problemTags.all():
                        selectProblem.add(problem)

            return list(selectProblem)
