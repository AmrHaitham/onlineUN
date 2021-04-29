from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class courses(models.Model):
    name = models.CharField(blank=True, max_length=50)
    hours = models.CharField(blank=True, max_length=50)
    totalDegree = models.IntegerField(blank=True, null=True)
    description=models.CharField(blank=True,null=True, max_length=1000)

    def __str__(self):
        return str(self.name)

class colage(models.Model):
    name = models.CharField(unique=True,max_length=50)
    colage_courses= models.ManyToManyField('courses')

    def __str__(self):
        return str(self.name)

class student(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    year = models.IntegerField(blank=True, null=True)

    student_colage=models.ForeignKey('colage',on_delete=models.CASCADE)
    birthday = models.DateField(blank=False, null=False)

    @property
    def get_phone(self):
        return phoneNumber.objects.filter(user_PhoneNumber=self.user)

    def __str__(self):
        return str(self.user.username)


class doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department = models.CharField(blank=False,max_length=50)
    doctor_colage= models.ManyToManyField('colage')
    birthday = models.DateField(blank=False, null=False)

    @property
    def get_phone(self):
        return phoneNumber.objects.filter(user_PhoneNumber=self.user)


    def __str__(self):
        return str(self.user.username)

class phoneNumber(models.Model):
    user_PhoneNumber=models.ForeignKey(User ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)

    def __str__(self):
        return str(self.user_PhoneNumber.username)

class assignment(models.Model):
    name = models.CharField(unique=True, max_length=50)
    file = models.FileField(upload_to='assignments/')
    dueTime = models.DateTimeField()
    uploadTime = models.DateTimeField(auto_now_add=True)
    totalDegree = models.IntegerField(blank=True, null=True)
    assignment_doctor=models.ForeignKey('doctor',on_delete=models.CASCADE)
    course_name=models.ForeignKey('courses',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class studentAssignmentAnswers(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(assignment, on_delete=models.CASCADE)
    answers= models.FileField(upload_to='assignmentsAnswers/')
    mark=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.student.user.username)



class lectures(models.Model):
    name = models.CharField(blank=True,max_length=50)
    file = models.FileField(upload_to='lecturesFile/')
    video = models.FileField(upload_to='lecturesVideo/', validators=[FileExtensionValidator(allowed_extensions=['mp4','avi', 'ogg', 'mov', 'flv', 'm4v', 'm4p', 'mpg', 'wmv', 'swf', 'mkv'])])
    uploadTime=models.DateTimeField(auto_now_add=True)
    course_name=models.ForeignKey('courses',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
