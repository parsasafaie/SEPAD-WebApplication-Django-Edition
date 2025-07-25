from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('downloads/', views.downloads, name='downloads'),
    path('contact/', views.contact, name='contact'),
    path('comings_soon/', views.comings_soon, name='comings_soon'),
    path('page_404/', views.page_404, name='page_404'),
    path('page_429/', views.page_429, name='page_429'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('duplicated_school_info/', views.duplicated_school_info, name='duplicated_school_info'),
    path('notify_username_password/', views.notify_username_password, name='notify_username_password'),
    path('unknown_school_info/', views.unknown_school_info, name='unknown_school_info'),
    path('panel/', views.panel_entry, name='panel_entry'),
    path('panel/school_info', views.school_info, name='school_info'),
    path('panel/classes', views.classes, name='classes'),
    path('panel/classes/add_class', views.add_class, name='add_class'),
    path('panel/classes/add_classes_from_excel', views.add_classes_from_excel, name='add_classes_from_excel'),
    path('panel/classes/class_file_permission_error', views.class_file_permission_error, name='class_file_permission_error'),
    path('panel/classes/duplicated_class_info', views.duplicated_class_info, name='duplicated_class_info'),
    path('panel/classes/error_in_class_excel', views.error_in_class_excel, name='error_in_class_excel'),
    path('panel/classes/unknown_class_info', views.unknown_class_info, name='unknown_class_info'),
    path('panel/classes/error_in_schedule', views.error_in_schedule, name='error_in_schedule'),
    path('panel/classes/class_info/<str:class_name>', views.class_info, name='class_info'),
    path('panel/classes/edit_class/<str:class_name>', views.edit_class, name='edit_class'),
    path('panel/classes/remove_class/<str:class_name>', views.remove_class, name='remove_class'),
    path('panel/teachers', views.teachers, name='teachers'),
    path('panel/teachers/add_teacher', views.add_teacher, name='add_teacher'),
    path('panel/teachers/teacher_info/<str:national_code>', views.teacher_info, name='teacher_info'),
    path('panel/teachers/wrong_teacher_info', views.wrong_teacher_info, name='wrong_teacher_info'),
    path('panel/teachers/edit_teacher/<str:national_code>', views.edit_teacher, name='edit_teacher'),
    path('panel/teachers/remove_teacher/<str:national_code>', views.remove_teacher, name='remove_teacher'),
    path('panel/students', views.students, name='students'),
    path('panel/students/add_student', views.add_student, name='add_student'),
    path('panel/students/student_file_permission_error', views.student_file_permission_error, name='student_file_permission_error'),
    path('panel/students/duplicated_student_info', views.duplicated_student_info, name='duplicated_student_info'),
    path('panel/students/error_in_student_excel', views.error_in_student_excel, name='error_in_student_excel'),
    path('panel/students/unknown_student_info', views.unknown_student_info, name='unknown_student_info'),
    path('panel/students/add_students_from_excel', views.add_students_from_excel, name='add_students_from_excel'),
    path('panel/students/edit_student/<str:national_code>', views.edit_student, name='edit_student'),
    path('panel/students/remove_student/<str:national_code>', views.remove_student, name='remove_student'),
    path('panel/students/student_info/<str:national_code>', views.student_info, name='student_info'),
]
