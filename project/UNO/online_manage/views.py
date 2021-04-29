from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.core.files.storage import FileSystemStorage

def getGroup(request):
    if request.user.groups.filter(name='admin').exists():
        usergroup = 'admin'
    if request.user.groups.filter(name='doctors').exists():
        usergroup = 'doctor'
    elif request.user.groups.filter(name='student').exists():
        usergroup = 'student'
    return usergroup


def base(request):
    return render(request,'online_manage/base.html')

def list_students(request):
    if getGroup(request) == 'student':
        user = get_object_or_404(User, username=request.user.username)
        students = get_object_or_404(student, user=user)
    else:
        students = student.objects.all()

    context ={
    'students' : students ,
    'group' : getGroup(request)
    }
    return render(request,'online_manage/students/list_students.html',context)

def add_students(request):
    if request.method == "POST" :
        user = User.objects.create_user(
            username=request.POST.get('user_name'),
            password=request.POST.get('password'),
            email =request.POST.get('email'),
            first_name=request.POST.get('name'),
            last_name=request.POST.get('last_name'),
            is_staff=True
        )
        students = student.objects.create(
            user = user ,
            year=request.POST.get('birthday'),
            birthday=request.POST.get('birthday'),
            student_colage = colage.objects.get(name=request.POST.get('colage'))
        )
        for phone in request.POST.getlist('phone'):
            phoneNumber.objects.create(
                user_PhoneNumber=students.user,
                phone=phone
                )
    return render(request,'online_manage/students/add_students.html')

def edit_students(request):
    user = get_object_or_404(User, username=request.user.username)
    studentdata = get_object_or_404(student, user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('name')
        user.last_name= request.POST.get('last_name')
        if user.check_password(request.POST.get('old_password')) :
            user.set_password(request.POST.get('password'))
        else :
            return HttpResponse("old password not correct")
        date = request.POST.get('birthday').split('-')
        new_date = f"{date[2]}-{date[0]}-{date[1]}"
        studentdata.birthday = new_date
        user.email= request.POST.get('email')
    user.save()
    studentdata.save()
    context={
    'user':user,
    'student':studentdata
    }
    return render(request,'online_manage/students/edit_student.html',context)

def list_doctors(request):
    user = get_object_or_404(User , username=request.user.username)
    if getGroup(request) == 'doctor' :
        doctorsdata= get_object_or_404(doctor, user=user)
    elif getGroup(request) == 'student' :
        studentdata=get_object_or_404(student, user=user)
        doctorsdata = doctor.objects.filter(doctor_colage=studentdata.student_colage)
    context={
    'doctors':doctorsdata,
    'group':getGroup(request)
    }
    return render(request,'online_manage/doctors/list_doctors.html',context)

def edit_doctor(request):
    user = get_object_or_404(User , username =request.user.username)
    doctordata= get_object_or_404(doctor,user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('name')
        user.last_name= request.POST.get('last_name')
        if user.check_password(request.POST.get('old_password')) :
            user.set_password(request.POST.get('password'))
        else :
            return HttpResponse("old password not correct")
        date = request.POST.get('birthday').split('-')
        new_date = f"{date[2]}-{date[0]}-{date[1]}"
        doctordata.birthday = new_date
        user.email= request.POST.get('email')
        doctordata.department=request.POST.get('department')
    user.save()
    doctordata.save()
    context={
    'user':user,
    'doctor':doctordata
    }
    return render(request,'online_manage/doctors/edit_doctor.html',context)

def list_assigenments(request):
    user = get_object_or_404(User , username=request.user.username)
    studentData=''
    doctorData=''
    if getGroup(request) == 'student' :
        studentData = get_object_or_404(student , user = user)
        colageData = colage.objects.get(name=studentData.student_colage)
        assignments = assignment.objects.filter(course_name__id__in=colageData.colage_courses.all())
    elif getGroup(request) == 'doctor':
        doctorData = get_object_or_404(doctor , user = user)
        assignments = assignment.objects.filter(assignment_doctor=doctorData)
        print(assignments)
    context= {
    'assignments':assignments ,
    'student':studentData,
    'doctor':doctorData,
    'group':getGroup(request)
    }
    return render(request,'online_manage/assignments/list_assignments.html',context)

def add_assignment(request):
    user = get_object_or_404(User,username=request.user.username)
    assignment_doctor= get_object_or_404(doctor , user=user)
    if request.method == "POST" and request.FILES['file']:
        date = request.POST.get('dueTime').split('-')
        new_date = f"{date[2]}-{date[0]}-{date[1]}"
        course_name=get_object_or_404(courses,name=request.POST.get('course_name'))
        new_assignment = assignment.objects.create(
            name =request.POST.get('name') ,
            file = request.FILES['file'] ,
            dueTime=new_date ,
            totalDegree=request.POST.get('totalDegree') ,
            assignment_doctor= assignment_doctor,
            course_name= course_name
        )

    return render(request,'online_manage/assignments/add_assignment.html')

def edit_assignment(request,ID):
    user = get_object_or_404(User,username=request.user.username)
    assignmentData = assignment.objects.get(name=ID)
    time = assignmentData.dueTime.strftime('%Y-%m-%d')
    if request.method == "POST" :
        assignmentData.name = request.POST.get('name')
        assignmentData.totalDegree = request.POST.get('totalDegree')
        if request.POST.get('dueTime') != assignmentData.dueTime :
            date = request.POST.get('dueTime').split('-')
            time = date
            assignmentData.dueTime = date
        assignmentData.course_name= get_object_or_404(courses,name=request.POST.get('course_name'))

    assignmentData.save()

    context = {
    'assignment':assignmentData,
    'time':time
    }
    return render(request,'online_manage/assignments/edit_assignment.html',context)
def courses_list(request):
    courses_list = ""
    if getGroup(request) == 'doctor' :
        doctordata = get_object_or_404(doctor , user=request.user)
        courses_list = courses.objects.filter(colage__in=doctordata.doctor_colage.all())
    elif getGroup(request) == 'student':
        studentData = get_object_or_404(student, user=request.user)
        colagedata = colage.objects.get(id=studentData.student_colage.id)
        courses_list = courses.objects.filter(colage=colagedata)
    context = {
        'courses':courses_list,
        'group':getGroup(request),

    }
    return render(request,'online_manage/courses/list_courses.html',context)
