from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User


class student_admin(admin.ModelAdmin):
    search_fields=['id']
    list_display =['id','user','year','student_colage','birthday']

    def get_queryset(self, request):
        qs = super(student_admin, self).get_queryset(request)
        if  request.user.is_superuser :
            return qs
        elif request.user.groups.filter(name='doctors').exists():
            return qs
        else :
            return qs.filter(user=request.user)

class doctor_admin(admin.ModelAdmin):
    search_fields=['id']
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ['id','user','department','Doctor_colage','birthday']
        else:
            self.list_display = ['user','department','Doctor_colage']

        return super(doctor_admin,self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super(doctor_admin, self).get_queryset(request)
        if  request.user.is_superuser :
            return qs
        else :
            return qs.filter(user=request.user)

    def Doctor_colage(self, obj):
        colages = []
        for colage in obj.doctor_colage.all():
            colages.append(colage.name)
        return ','.join(colages)


class colage_admin(admin.ModelAdmin):
    list_display=['id','name']
    search_fields=['id','name']

class courses_admin(admin.ModelAdmin):
    list_display=['id','name','hours','totalDegree']
    search_fields=['id','name']


class studentAssignmentAnswers_admin(admin.ModelAdmin):
    list_display=['student','assignment','mark']
    search_fields=['student__user__username']

    def get_queryset(self, request):
        qs = super(studentAssignmentAnswers_admin,self).get_queryset(request)
        if request.user.groups.filter(name='student').exists():
            return qs.filter(student__user=request.user)
        elif request.user.groups.filter(name='doctors').exists():
            assignmentdata = assignment.objects.filter(assignment_doctor__user=request.user)
            return qs.filter(assignment__id__in=assignmentdata)
        else : return qs


    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.groups.filter(name='student').exists():
            self.readonly_fields = ['mark']
        return super(studentAssignmentAnswers_admin,self).change_view(request, object_id, form_url='',extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.groups.filter(name='student').exists():
            self.readonly_fields = ['mark']
        return super(studentAssignmentAnswers_admin,self).add_view(request, form_url='',extra_context=extra_context)

class phoneNumber_admin(admin.ModelAdmin):
    list_display=['user_PhoneNumber','phone']
    def get_queryset(self, request):
        qs = super(phoneNumber_admin, self).get_queryset(request)
        return qs.filter(user_PhoneNumber=request.user)

class lectures_admin(admin.ModelAdmin):
    list_display = ["name","course_name"]
    # def get_queryset(self, request):
    #     qs = super(lectures_admin, self).get_queryset(request)
        # if request.user.groups.filter(name='student').exists():
        #     studentData = student.objects.filter(user=request.user)
        #     courses_list = courses.objects.filter(colage=studentData.student_colage)
        #     return qs.filter(course_name__in=courses_list.all())
        # elif request.user.groups.filter(name='doctors').exists():
        #     doctordata = doctor.objects.filter(user=request.user)
        #     courses_list = courses.objects.filter(colage__in=doctordata.doctor_colage.all())
        #     return qs.filter(course_name__in=courses_list.all())

admin.site.register(colage,colage_admin)
admin.site.register(student,student_admin)
admin.site.register(doctor,doctor_admin)
admin.site.register(studentAssignmentAnswers, studentAssignmentAnswers_admin)
admin.site.register(courses,courses_admin)
admin.site.register(assignment)
admin.site.register(phoneNumber,phoneNumber_admin)
admin.site.register(lectures,lectures_admin)
