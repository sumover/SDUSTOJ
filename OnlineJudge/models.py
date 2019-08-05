from django.db import models


# Create your models here.
class Organization(models.Model):
    orgName = models.CharField(max_length=100)
    shortName = models.CharField(max_length=20)


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Student(User):
    nickname = models.CharField(max_length=20)
    creator = models.ForeignKey(to='Administrator', on_delete=models.DO_NOTHING)
    create_date = models.DateField(auto_now_add=True)


class UserRole(models.Model):
    role = models.CharField(max_length=100)


class Administrator(User):
    role = models.ForeignKey(to='UserRole', on_delete=models.DO_NOTHING)


class OrganizationAdministrator(Administrator):
    pass


class SuperAdministrator(Administrator):
    pass


class GeneralAdministrator(Administrator):
    subOrganization = models.ForeignKey(to='Organization', on_delete=models.CASCADE)


class Matter(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)


class Squad(Matter):
    squadName = models.CharField(max_length=100)
    students = models.ManyToManyField(to='Student')
    courses = models.ManyToManyField(to='Course')
    subOrg = models.ForeignKey(to='Organization', on_delete=models.CASCADE)


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


class Contest(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    beginTime = models.DecimalField(max_digits=32, decimal_places=9)
    endTime = models.DecimalField(max_digits=32, decimal_places=9)
    contestproblems = models.ManyToManyField(to='Problem')
    config = models.ForeignKey(ContestConfig, on_delete=models.DO_NOTHING)
    participateCourse = models.ForeignKey(Course, on_delete=models.DO_NOTHING)


class SubmissionStatus(Matter):
    aimSubmission = models.OneToOneField(to='Submission', on_delete=models.CASCADE)
    status = models.IntegerField()  # -1 ,0 ,1
    result = models.CharField(max_length=20, blank=True)
    judgingMessage = models.CharField(max_length=10000, blank=True)


class Problem(models.Model):
    creator = models.ForeignKey(Administrator, on_delete=models.DO_NOTHING)
    createTime = models.DateTimeField(auto_now_add=True)
    problemName = models.CharField(max_length=100)
    shortName = models.CharField(max_length=100)
    problemDetail = models.BinaryField(max_length=10 * 1024 * 1024)
    testCases = models.ManyToManyField(to="TestCase")


class Tag(models.Model):
    creator = models.ForeignKey(Administrator, on_delete=models.DO_NOTHING)
    tagRole = models.CharField(max_length=100)
