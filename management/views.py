from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from .models import School, Class, Teacher, Student
from utils.excel_reading import add_classes, add_students
from utils.generate_class_code import generate_class_code, reverse_class_code

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def downloads(request):
    return render(request, 'downloads.html')

def contact(request):
    return render(request, 'contact.html')

def comings_soon(request):
    return render(request, 'coming_soon.html')

def page_404(request):
    return render(request, '404.html')

def page_429(request):
    return render(request, '429.html')

def login_view(request):
    if request.method == 'POST':
        school_code = request.POST.get('school_code')
        manager_personal_code = request.POST.get('manager_personal_code')

        user = School.objects.filter(Q(school_code=school_code)&Q(manager_personal_code=manager_personal_code)).first()
        print(user)

        if user is not None:
            login(request, user)
            return redirect('panel_entry')
        else:
            return redirect('unknown_school_info')
            
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        school_code = request.POST.get('school_code')
        manager_personal_code = request.POST.get('manager_personal_code')
        province = request.POST.get('province')
        city = request.POST.get('city')
        email = request.POST.get('email')

        if School.objects.filter(Q(school_code=school_code) | Q(manager_personal_code=manager_personal_code)):
            return redirect('duplicated_school_info')

        School.objects.create_user(
            school_name=school_name,
            school_code=school_code,
            manager_personal_code=manager_personal_code,
            province=province,
            city=city,
            email=email
        )

        return redirect('notify_username_password')
    
    return render(request, 'signup.html')

def duplicated_school_info(request):
    return render(request, 'duplicated_school_info.html')

def notify_username_password(request):
    return render(request, 'notify_username_password.html')

def unknown_school_info(request):
    return render(request, 'unknown_school_info.html')

@login_required
def panel_entry(request):
    return render(request, 'panel_entry.html')

@login_required
def school_info(request):
    current_user = request.user
    
    cc = len(current_user.classes.all())
    tc = len(current_user.teachers.all())
    sc = len(current_user.students.all())
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    return render(request, 'school_info.html', {'data':current_user, 'cc':cc, 'tc':tc, 'sc':sc})

@login_required
def classes(request):
    current_user = request.user
    classes = current_user.classes.all()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    return render(request, 'classes.html', {'classes':classes})

@login_required
def add_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')

        current_user = request.user
        school_code = current_user.school_code

        class_code=generate_class_code(school_code, class_name)
        if Class.objects.filter(class_code=class_code):
            return redirect('duplicated_class_info')
        
        Class.objects.create(class_name=class_name, 
                            class_code=class_code,
                            school=current_user)
        
        return redirect('classes')

    return render(request, 'add_class.html')

@login_required
def add_classes_from_excel(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        sheet_name = request.POST.get('sheet')
        name_letter = request.POST.get('name')

        classes = Class.objects.all()
        school_user = request.user

        result = add_classes(filename, sheet_name, name_letter, [cls.class_name for cls in classes], school_user.school_code)
        
        if result == 'sheet_not_found':
            return redirect('error_in_class_excel')

        if result == 'bad_column_letter':
            return redirect('error_in_class_excel')

        if isinstance(result[0], list):
            return redirect('error_in_class_excel')
        
        for cls in result:
            Class.objects.create(
                class_name=cls['name'],
                class_code=cls['code'],
                school_id=school_user.id,
            )

        return redirect('classes')

    return render(request, 'add_classes_from_excel.html')

@login_required
def class_info(request, class_name):
    current_user  = request.user
    data = Class.objects.filter(Q(class_name=class_name) & Q(school=current_user.id)).first()

    if data is None:
        return redirect(unknown_class_info)

    return render(request, 'class_info.html', {'data':data, 'teachers':data.teachers.all(), 'students':data.students.all()})

@login_required
def edit_class(request, class_name):
    current_user  = request.user
    data = Class.objects.filter(Q(class_name=class_name) & Q(school=current_user.id)).first()

    if data is None:
        return redirect(unknown_class_info)
    
    if request.method == 'POST':
        new_name = request.POST.get("class_name")

        if new_name==class_name:
            return redirect('classes')
        
        if Class.objects.filter(Q(class_name=new_name) & Q(school=current_user.id)):
            return redirect('duplicated_class_info')

        new_code = generate_class_code(current_user.school_code, new_name)

        data.class_name = new_name
        data.class_code = new_code
        data.save()

        return redirect('classes')


    return render(request, 'edit_class.html', {'name':data.class_name})

def remove_class(request, class_name):
    current_user = request.user

    cls = Class.objects.filter(Q(class_name=class_name)&Q(school=current_user.id)).first()
    if cls is None:
        return redirect('unknown_student_info')

    Class.delete(cls)
        
    return redirect('classes')


def duplicated_class_info(request):
    return render(request, 'duplicated_class_info.html')

def error_in_class_excel(request):
    return render(request, 'error_in_class_excel.html')

def class_file_permission_error(request):
    return render(request, 'class_file_permission_error.html')

def unknown_class_info(request):
    return render(request, 'unknown_class_info.html')

def error_in_schedule(request):
    return render(request, 'error_in_schedule.html')

def teachers(request):
    currect_user = request.user
    teachers = currect_user.teachers.all()
    return render(request, 'teachers.html', {'teachers':teachers})

def add_teacher(request):
    current_user = request.user
    if request.method == 'POST':
        national_code = request.POST.get('teacher_national_code')
        password = request.POST.get('teacher_password')

        teacher = Teacher.objects.filter(Q(teacher_national_code=national_code)  & Q(teacher_password=password)).first()
        if teacher is None:
            return redirect('wrong_teacher_info')
        
        classes = request.POST.getlist('selected_classes')
        for class_id in classes:
            cls = Class.objects.filter(id=int(class_id)).first()
            cls.teachers.add(teacher)

        current_user.teachers.add(teacher)
        
        return redirect('teachers')
    
    school_classes = current_user.classes.all()
    return render(request, 'add_teacher.html', {'classes':school_classes})

def teacher_info(request, national_code):
    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')
    
    current_user = request.user
    school_teachers = current_user.teachers.all()

    if not (teacher in school_teachers):
        return redirect('wrong_teacher_info')

    return render(request, 'teacher_info.html', {'data':teacher})

def wrong_teacher_info(request):
    return render(request, 'wrong_teacher_info.html')

def edit_teacher(request, national_code):
    current_user = request.user
    if request.method == 'POST':
        new_classes = request.POST.getlist('selected_classes')
        if new_classes == []:
            return redirect('teachers')

        teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
        if teacher is None:
            return redirect('wrong_teacher_info')
        
        teacher_classes = teacher.classes.all()
        for cls in teacher_classes:
            class_code = cls.class_code
            class_school_code = reverse_class_code(class_code)[0]
            if class_school_code == current_user.school_code:
                teacher.classes.remove(cls)
        
        for cls_code in new_classes:
            cls = Class.objects.filter(class_code=cls_code).first()
            teacher.classes.add(cls)
        
        return redirect('teachers')


    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')

    school_teachers = current_user.teachers.all()
    school_classes = current_user.classes.all()

    if not (teacher in school_teachers):
        return redirect('wrong_teacher_info')
    
    return render(request, 'edit_teacher.html', {'teacher':teacher, 'classes':school_classes})

def remove_teacher(request, national_code):
    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')
    
    current_user = request.user
    school_teachers = current_user.teachers.all()

    if not (teacher in school_teachers):
        return redirect('wrong_teacher_info')
    
    teacher_classes = teacher.classes.all()
    for cls in teacher_classes:
        class_code = cls.class_code
        class_school_code = reverse_class_code(class_code)[0]
        if class_school_code == current_user.school_code:
            teacher.classes.remove(cls)

    current_user.teachers.remove(teacher)

    return redirect(request, 'teachers.html')

def students(request):
    currect_user = request.user
    students = currect_user.students.all()
    return render(request, 'students.html', {'students':students})

def add_student(request):
    current_user = request.user
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_family = request.POST.get('student_family')
        student_national_code = request.POST.get('student_national_code')
        student_password = request.POST.get('student_password')
        student_phone_number = request.POST.get('student_phone_number')

        selected_class_code = request.POST.get('selected_class')

        if Student.objects.filter(Q(student_national_code=student_national_code) | Q(student_phone_number=student_phone_number)):
            return redirect('add_student')

        Student.objects.create(student_name=student_name,
                               student_family=student_family,
                               student_national_code=student_national_code,
                               student_password=student_password,
                               student_phone_number=student_phone_number,
                               student_class=Class.objects.get(id=int(selected_class_code)),
                               school=current_user)
        
        return redirect('students')

    return render(request, 'add_student.html', {'classes':current_user.classes.all()})

def duplicated_student_info(request):
    return render(request, 'duplicated_student_info.html')

def error_in_student_excel(request):
    return render(request, 'error_in_student_excel.html')

def student_file_permission_error(request):
    return render(request, 'student_file_permission_error.html')

def unknown_student_info(request):
    return render(request, 'unknown_student_info.html')

@login_required
def add_students_from_excel(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        sheet_name = request.POST.get('sheet')
        name_letter = request.POST.get('name')
        family_letter = request.POST.get('family')
        nc_letter = request.POST.get('national_code')
        class_letter = request.POST.get('class')
        pass_letter = request.POST.get('password')
        phone_letter = request.POST.get('phone_number')

        classes = Class.objects.all()
        students = Student.objects.all()
        school_user = request.user

        result = add_students(filename, sheet_name, name_letter, family_letter, nc_letter, class_letter, pass_letter, phone_letter,
                              [cls.class_name for cls in classes],
                              [student.student_national_code for student in students],
                              [student.student_phone_number for student in students],
                              school_user.school_code)
        
        if result == 'sheet_not_found':
            return redirect('error_in_student_excel')

        if result == 'bad_column_letter':
            return redirect('error_in_student_excel')
        
        if isinstance(result[0], list):
            excel_errors = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    excel_errors.append(f"Bad data format in cell {cell}.")
                elif problem[0] == "duplicated_nc":
                    excel_errors.append(
                        f"Duplicated national code in cell {cell}.")
                elif problem[0] == 'unknown_class':
                    excel_errors.append(f"Unknown class name in cell {cell}.")
                else:
                    excel_errors.append(f"Unknown issue in cell {cell}.")

            print(excel_errors)
            return redirect('error_in_student_excel')
        
        for student in result:
            cls = Class.objects.filter(class_code=student['class']).first()
            Student.objects.create(
                student_name=student['name'],
                student_family=student['family'],
                student_national_code=student['national_code'],
                student_phone_number=student['phone_number'],
                student_class=cls,
                student_password=student['password'],
                school_id=school_user.id
            )
            
        return redirect('students')

    return render(request, 'add_students_from_excel.html')

def edit_student(request, national_code):
    current_user = request.user

    student = Student.objects.filter(Q(student_national_code=national_code)&Q(school_id=current_user.id)).first()
    if student is None:
        return redirect('unknown_student_info')
    
    if request.method == 'POST':
        student_name = request.POST.get("student_name")
        student_family = request.POST.get("student_family")
        student_national_code = request.POST.get("student_national_code")
        student_password = request.POST.get("student_password")
        student_phone_number = request.POST.get("student_phone_number")

        if Student.objects.filter(Q(student_national_code=student_national_code) & Q(student_phone_number=student_phone_number)):
            return redirect('duplicated_student_info')

        student.name = student_name
        student.student_family = student_family
        student.student_national_code = student_national_code
        student.student_password = student_password
        student.student_phone_number = student_phone_number

        student.save()
        
        return redirect('students')
    
    return render(request, 'edit_student.html', {'student': student})

def remove_student(request, national_code):
    current_user = request.user

    student = Student.objects.filter(Q(student_national_code=national_code)&Q(school_id=current_user.id)).first()
    if student is None:
        return redirect('unknown_student_info')

    Student.delete(student)
        
    return redirect('students')

def student_info(request, national_code):
    current_user = request.user

    student = Student.objects.filter(Q(student_national_code=national_code)&Q(school_id=current_user.id)).first()
    if student is None:
        return redirect('unknown_student_info')

    return redirect('student_info', {'data':student})
    