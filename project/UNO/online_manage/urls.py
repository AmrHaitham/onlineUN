from django.urls import path
from . import views


app_name ='online_manage' # used in html only and path name
urlpatterns = [
    path('base/',views.base,name='base'),
    path('students/',views.list_students,name='students'),
    path('add_students/',views.add_students,name='add_students'),
    path('edit_students/',views.edit_students,name='edit_students'),
    path('doctors/',views.list_doctors,name='doctors'),
    path('edit_doctor',views.edit_doctor,name='edit_doctor'),
    path('list_assigenments',views.list_assigenments,name='list_assignments'),
    path('add_assignment',views.add_assignment,name='add_assignment'),
    path('edit_assignment/<ID>/',views.edit_assignment,name='edit_assignment'),
    path('list_courses/',views.courses_list,name='list_course')
]
