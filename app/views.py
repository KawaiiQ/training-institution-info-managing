from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as _logout
from django.http import HttpResponse

from .models import User as _User, Tutor as _Tutor, Admin as _Admin
from .models import Course as _Course, Teacher as _Teacher, Student as _Student
from .models import CourseSelect as _Select
from .models import ClassRecord as _Record
from .models import TeacherRecord as _TeacherRecord
from .transactions import User as _UserOperation

from json import dumps


def user_info(request):
    user = request.user
    if user.is_authenticated():
        user.is_tutor = _Tutor.objects.filter(user=user).exists()
        user.is_admin = _Admin.objects.filter(user=user).exists()
    return user


def homepage(request):
    return render(request, 'homepage.html', {
        'user': user_info(request)
    })


def loginpage(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponse('你已经登陆过')
        return render(request, 'loginpage.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'loginpage.html', {
                'failed': True,
            })


def passwordpage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    if request.method == 'GET':
        return render(request, 'passwordpage.html', {
           'user': user_info(request)
        })
    else:
        succeeded = True
        reason = None

        username = request.user
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        confirmation = request.POST['confirmation']

        user = authenticate(username=username, password=old_password)
        if user is not None:
            if new_password == confirmation:
                user = request.user
                user.set_password(new_password)
                user.save()
            else:
                succeeded = False
                reason = 'ns'
        else:
            succeeded = False
            reason = 'wp'

        return render(request, 'passwordpage.html', {
           'user': user_info(request),
           'result': True,
           'succeeded': succeeded,
           'reason': reason
        })


def logout(request):
    if request.user.is_authenticated():
        _logout(request)
        return redirect('/')
    else:
        return HttpResponse('你尚未登录')


def tutorpage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')

    tutors = _Tutor.objects.all()

    if request.method == 'GET':
        return render(request, 'tutorpage.html', {
           'user': user_info(request),
           'tutors': tutors
        })
    else:
        error = False
        reason = None

        username = request.POST['username']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        name = request.POST['name']
        phone = request.POST['phone']

        if username == '':
            error = True
            reason = '用户名不可为空'
        elif name == '':
            error = True
            reason = '姓名不可为空'
        elif password != confirmation:
            error = True
            reason = '两次密码输入不一致'
        elif _User.objects.filter(username=username):
            error = True
            reason = '该用户名已经存在'
        else:
            _UserOperation.create_tutor(username, password, name, phone)

        return render(request, 'tutorpage.html', {
           'user': user_info(request),
           'tutors': tutors,
           'post': True,
           'error': error,
           'reason': reason
        })


def edit_tutor(request, username):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return HttpResponse('你没有对应的权限')
    elif not _Tutor.objects.filter(user__username=username).exists():
        return HttpResponse('没有找到响应的班主任')

    user = _User.objects.filter(username=username).first()
    tutor = user.tutor

    if request.method == 'GET':
        return render(request, 'tutoreditpage.html', {
            'user': user_info(request),
            'tutor': tutor,
            'tutor_user': user,
        })
    else:
        error = False
        reason = None

        post = request.POST

        if 'name' in post and 'phone' in post:
            if post['name'] == '':
                error = True
                reason = '姓名不可为空'
            else:
                tutor.name = post['name']
                tutor.phone = post['phone']
                tutor.save()

        if 'newPassword' in post and 'confirmation' in post:
            new_passwd = post['newPassword']
            confirmation = post['confirmation']
            if new_passwd != confirmation:
                error = True
                reason = '两次密码输入不一致'
            else:
                user.set_password(new_passwd)
                user.save()

        return render(request, 'tutoreditpage.html', {
            'user': user_info(request),
            'tutor': tutor,
            'tutor_user': user,
            'post': True,
            'error': error,
            'reason': reason
        })


def delete_tutor(request, username):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return HttpResponse('你没有对应的权限')
    elif not _Tutor.objects.filter(user__username=username).exists():
        return HttpResponse('没有找到响应的班主任')

    user = _User.objects.filter(username=username).first()
    if user is None:
        return HttpResponse('用户不存在')
    user.delete()

    return redirect('/tutor/')


def teacherpage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif (not _Admin.objects.filter(user=request.user).exists()) and \
            (not _Tutor.objects.filter(user=request.user).exists()):
        return redirect('/')

    teachers = _Teacher.objects.all()

    post = False
    error = False
    reason = None

    if request.method == 'POST' and _Admin.objects.filter(user=request.user).exists():
        post = True
        name = request.POST['name']
        phone = request.POST['phone']
        time = request.POST['time']
        if name == '':
            error = True
            reason = '教师姓名不可为空'
        else:
            if time == '':
                time = 0
            teacher = _Teacher(name=name, phone=phone, time=time)
            teacher.save()

    return render(request, 'teacherpage.html', {
        'user': user_info(request),
        'teachers': teachers,
        'post': post,
        'error': error,
        'reason': reason,
    })


def edit_teacher(request, tid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Teacher.objects.filter(id=tid):
        return HttpResponse('没有找到对应科目')

    teacher = _Teacher.objects.filter(id=tid).first()

    post = False
    error = False
    reason = None

    if request.method == 'POST':
        post = True
        name = request.POST['name']
        phone = request.POST['phone']
        time = request.POST['time']
        if name == '':
            error = True
            reason = '教师姓名不可为空'
        else:
            if time == '':
                time = 0
            teacher.name = name
            teacher.phone = phone
            teacher.time = time
            teacher.save()

    return render(request, 'teachereditpage.html', {
        'user': user_info(request),
        'teacher': teacher,
        'post': post,
        'error': error,
        'reason': reason
    })


def delete_teacher(request, tid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Teacher.objects.filter(id=tid):
        return HttpResponse('没有找到对应教师')

    teacher = _Teacher.objects.filter(id=tid).first()
    teacher.delete()

    return redirect('/teacher/')


def coursepage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')

    courses = _Course.objects.all()

    if request.method == 'GET':
        return render(request, 'coursepage.html', {
            'user': user_info(request),
            'courses': courses
        })
    else:
        error = False
        reason = None

        name = request.POST['name']
        index = request.POST['index']

        if name == '':
            error = True
            reason = '科目名称不可为空'
        if index == '':
            error = True
            reason = '索引不可为空'
        else:
            course = _Course(name=name, index=index)
            course.save()

        return render(request, 'coursepage.html', {
            'user': user_info(request),
            'courses': courses,
            'post': True,
            'error': error,
            'reason': reason
        })


def edit_course(request, cid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')

    course = _Course.objects.filter(id=cid).first()
    teachers = _Teacher.objects.filter(course=course)
    all_teachers = _Teacher.objects.all()

    if request.method == 'GET':
        return render(request, 'courseeditpage.html', {
            'user': user_info(request),
            'course': course,
            'teachers': teachers,
            'all_teachers': all_teachers
        })
    else:
        error = False
        reason = None

        post = dict(request.POST)

        if 'course-name' in post:
            name = post['course-name']
            index = post['course-index']
            if name == '':
                error = True
                reason = '科目名称不可为空'
            elif index == '':
                error = True
                reason = '科目索引不可为空'
            else:
                course.name = name
                course.save()
        elif 'teacher_id' in post:
            teachers = post['teacher_id']
            for i in teachers:
                tid = int(i)
                teacher = _Teacher.objects.filter(id=tid).first()
                if teacher is not None and not course.teacher.filter(id=tid).exists():
                    course.teacher.add(teacher)
                    course.teacher_num += 1
            course.save()

        teachers = _Teacher.objects.filter(course=course)

        return render(request, 'courseeditpage.html', {
            'user': user_info(request),
            'course': course,
            'teachers': teachers,
            'all_teachers': all_teachers,
            'post': True,
            'error': error,
            'reason': reason
        })


def delete_course_teacher(request, cid, tid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')
    elif not _Teacher.objects.filter(id=tid):
        return HttpResponse('没有找到对应教师')

    course = _Course.objects.filter(id=int(cid)).first()
    teacher = _Teacher.objects.filter(id=int(tid)).first()

    if course.teacher.filter(id=tid).exists():
        course.teacher.remove(teacher)
        course.teacher_num -= 1
        course.save()

    return redirect('/edit-course/'+str(course.id)+'/')


def delete_course(request, cid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')

    course = _Course.objects.filter(id=cid).first()
    course.delete()

    return redirect('/course/')


def studentpage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif (not _Admin.objects.filter(user=request.user).exists()) and\
            (not _Tutor.objects.filter(user=request.user).exists()):
        return redirect('/')

    tutors = _Tutor.objects.all()
    choices = _Student.TYPE_CHOICES
    students = _Student.objects.all()
    post = False
    error = False
    reason = None
    search = ''

    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET['search']
        students = students.filter(name__contains=search)

    elif request.method == 'POST':
        post = True

        name = request.POST['name']
        stype = request.POST['type']
        tutor = request.POST['tutor']

        if name == '':
            error = True
            reason = '姓名不能为空'
        elif stype == '':
            error = True
            reason = '类型不能为空'
        elif tutor == '':
            error = True
            reason = '班主任不能为空'
        else:
            tutor = _Tutor.objects.filter(id=int(tutor)).first()
            if tutor is None:
                error = True
                reason = '未找到对应的班主任'
            else:
                student = _Student(name=name, type=int(stype), tutor=tutor)
                student.save()

    return render(request, 'studentpage.html', {
        'user': user_info(request),
        'students': students,
        'post': post,
        'error': error,
        'reason': reason,
        'choices': choices,
        'tutors': tutors,
        'search': search
    })


def edit_student(request, sid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif (not _Admin.objects.filter(user=request.user).exists()) and \
            (not _Tutor.objects.filter(user=request.user).exists()):
        return redirect('/')
    elif not _Student.objects.filter(id=sid).exists():
        return HttpResponse('未找到对应学生')

    student = _Student.objects.filter(id=sid).first()
    choices = _Student.TYPE_CHOICES
    tutors = _Tutor.objects.all()
    courses = _Course.objects.all()
    selects = _Select.objects.filter(student=student)
    post = False
    error = False
    reason = None

    if request.method == 'POST' and _Admin.objects.filter(user=request.user).exists():
        post = True

        if 'course-id' in request.POST or 'course-teacher' in request.POST or 'course-time' in request.POST:
            cid = request.POST['course-id']
            tid = request.POST['course-teacher']
            time = request.POST['course-time']
            if cid == '':
                error = True
                reason = '课程不可为空'
            elif tid == '':
                error = True
                reason = '教师不可为空'
            elif time == '':
                error = True
                reason = '课时不可为空'
            else:
                course = _Course.objects.filter(id=cid).first()
                teacher = _Teacher.objects.filter(id=tid).first()
                if _Select.objects.filter(student=student, course=course).exists():
                    error = True
                    reason = '已选择该门课程'
                elif course is None:
                    error = True
                    reason = '找不到对应课程'
                elif teacher is None:
                    error = True
                    reason = '找不到对应教师'
                else:
                    select = _Select(course=course, student=student, teacher=teacher, time=time)
                    select.save()
        else:
            if not _Admin.objects.filter(user=request.user):
                return HttpResponse('没有权限')

            name = request.POST['name']
            stype = request.POST['type']
            tutor = request.POST['tutor']

            if name == '':
                error = True
                reason = '姓名不能为空'
            elif stype == '':
                error = True
                reason = '类型不能为空'
            elif tutor == '':
                error = True
                reason = '班主任不能为空'
            else:
                _tutor = _Tutor.objects.filter(id=int(tutor)).first()
                if tutor is None:
                    error = True
                    reason = '未找到对应的班主任'
                else:
                    student.name = name
                    student.type = stype
                    student.tutor = _tutor
                    student.save()

    student = _Student.objects.filter(id=sid).first()

    return render(request, 'studenteditpage.html', {
        'user': user_info(request),
        'student': student,
        'choices': choices,
        'tutors': tutors,
        'post': post,
        'error': error,
        'reason': reason,
        'courses': courses,
        'selects': selects
    })


def delete_student(request, sid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Student.objects.filter(id=sid).exists():
        return HttpResponse('未找到对应学生')

    student = _Student.objects.filter(id=int(sid))
    student.delete()

    return redirect('/student/')


def course_teacher(request, cid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif (not _Admin.objects.filter(user=request.user).exists()) and \
            (not _Tutor.objects.filter(user=request.user).exists()):
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')

    course = _Course.objects.filter(id=cid).first()
    teachers = course.teacher.all()

    string = dumps(list(teachers.values('id', 'name', 'phone')))

    return HttpResponse(string)


def delete_select(request, sid, cid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')
    elif not _Student.objects.filter(id=sid):
        return HttpResponse('没有找到对应学生')

    student = _Student.objects.filter(id=sid).first()
    course = _Course.objects.filter(id=cid).first()

    _Select.objects.filter(student=student, course=course).delete()

    return redirect('/edit-student/' + str(student.id) + '/')


def add_time(request, sid, cid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')
    elif not _Student.objects.filter(id=sid):
        return HttpResponse('没有找到对应学生')

    student = _Student.objects.filter(id=sid).first()
    course = _Course.objects.filter(id=cid).first()

    select = _Select.objects.filter(student=student, course=course).first()
    select.time += 1
    select.save()

    return redirect('/edit-student/' + str(student.id) + '/')


def sub_time(request, sid, cid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Course.objects.filter(id=cid):
        return HttpResponse('没有找到对应科目')
    elif not _Student.objects.filter(id=sid):
        return HttpResponse('没有找到对应学生')

    student = _Student.objects.filter(id=sid).first()
    course = _Course.objects.filter(id=cid).first()

    select = _Select.objects.filter(student=student, course=course).first()
    select.time -= 1
    select.save()

    return redirect('/edit-student/' + str(student.id) + '/')


def classpage(request, sid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif (not _Admin.objects.filter(user=request.user).exists()) and \
            (not _Tutor.objects.filter(user=request.user).exists()):
        return redirect('/')
    elif not _Student.objects.filter(id=sid):
        return HttpResponse('没有找到对应学生')

    student = _Student.objects.filter(id=int(sid)).first()
    records = _Record.objects.filter(student=student)

    post = False
    error = False
    reason = None

    if request.method == 'POST':
        post = True
        data = request.POST

        school = data.get('school')
        grade = data.get('grade')
        course = data.get('course')
        book = data.get('book')
        unit = data.get('unit')
        study = data.get('study')
        knowledge = data.get('knowledge')
        practice = data.get('practice')
        note = data.get('note')
        study_note = data.get('study_note')
        date = data.get('date')

        if (not school) or (not grade) or (not course) or (not book) or (not unit) or (not date):
            error = True
            reason = '学习内容所有项均不得为空'
        elif (not study) or (not knowledge) or (not practice):
            error = True
            reason = '评价内容所有项均不得为空'
        else:
            record = _Record(
                student=student,
                school=int(school),
                grade=int(grade),
                course=int(course),
                book=int(book),
                unit=int(unit),
                note=note,
                study=int(study),
                knowledge=int(knowledge),
                practice=int(practice),
                study_note=study_note,
                date=date
            )
            record.save()

    return render(request, 'classpage.html', {
        'user': user_info(request),
        'student': student,
        'records': records,

        'post': post,
        'error': error,
        'reason': reason,

        'school_choices': _Record.SCHOOL_CHOICES,
        'grade_choices': _Record.GRADE_CHOICES,
        'course_choices': _Record.COURSE_CHOICES,
        'book_choices': _Record.BOOK_CHOICES,
        'unit_choices': _Record.UNIT_CHOICES,
        'study_choices': _Record.STUDY_CHOICES,
        'knowledge_choices': _Record.KNOWLEDGE_CHOICES,
        'practice_choices': _Record.PRACTICE_CHOICES
    })


def edit_class(request, rid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Record.objects.filter(id=int(rid)):
        return HttpResponse('没有找到对应记录')

    record = _Record.objects.filter(id=int(rid)).first()
    student = record.student

    post = False
    error = False
    reason = None

    if request.method == 'POST':
        post = True
        data = request.POST

        school = data.get('school')
        grade = data.get('grade')
        course = data.get('course')
        book = data.get('book')
        unit = data.get('unit')
        study = data.get('study')
        knowledge = data.get('knowledge')
        practice = data.get('practice')
        note = data.get('note')
        study_note = data.get('study_note')
        date = data.get('date')

        if (not school) or (not grade) or (not course) or (not book) or (not unit) or (not date):
            error = True
            reason = '学习内容所有项均不得为空'
        elif (not study) or (not knowledge) or (not practice):
            error = True
            reason = '评价内容所有项均不得为空'
        else:
            record.school = int(school)
            record.grade = int(grade)
            record.course = int(course)
            record.book = int(book)
            record.unit = int(unit)
            record.note = note
            record.study = int(study)
            record.knowledge = int(knowledge)
            record.practice = int(practice)
            record.study_note = study_note
            record.date = date
            record.save()

    record = _Record.objects.filter(id=int(rid)).first()

    return render(request, 'editclass.html', {
        'user': user_info(request),
        'student': student,
        'record': record,

        'post': post,
        'error': error,
        'reason': reason,

        'school_choices': _Record.SCHOOL_CHOICES,
        'grade_choices': _Record.GRADE_CHOICES,
        'course_choices': _Record.COURSE_CHOICES,
        'book_choices': _Record.BOOK_CHOICES,
        'unit_choices': _Record.UNIT_CHOICES,
        'study_choices': _Record.STUDY_CHOICES,
        'knowledge_choices': _Record.KNOWLEDGE_CHOICES,
        'practice_choices': _Record.PRACTICE_CHOICES
    })


def delete_class(request, rid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Record.objects.filter(id=int(rid)):
        return HttpResponse('没有找到对应记录')

    record = _Record.objects.filter(id=int(rid)).first()
    student = record.student
    record.delete()

    return redirect('/class/' + str(student.id) + '/')


def add_teacher_time(request, tid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Teacher.objects.filter(id=tid):
        return HttpResponse('没有找到对应老师')

    teacher = _Teacher.objects.filter(id=tid).first()

    teacher.time += 1
    teacher.save()

    return redirect('/teacher/')


def sub_teacher_time(request, tid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Teacher.objects.filter(id=tid):
        return HttpResponse('没有找到对应老师')

    teacher = _Teacher.objects.filter(id=tid).first()

    teacher.time -= 1
    teacher.save()

    return redirect('/teacher/')


def teacherrecordpage(request, tid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _Teacher.objects.filter(id=tid):
        return HttpResponse('没有找到对应教师')

    teacher = _Teacher.objects.filter(id=int(tid)).first()
    records = _TeacherRecord.objects.filter(teacher=int(tid))

    post = False
    error = False
    reason = None

    if request.method == 'POST':
        post = True
        data = request.POST

        school = data.get('school')
        grade = data.get('grade')
        course = data.get('course')
        book = data.get('book')
        unit = data.get('unit')
        study = data.get('study')
        knowledge = data.get('knowledge')
        practice = data.get('practice')
        note = data.get('note')
        study_note = data.get('study_note')
        date = data.get('date')

        if (not school) or (not grade) or (not course) or (not book) or (not unit) or (not date):
            error = True
            reason = '学习内容所有项均不得为空'
        elif (not study) or (not knowledge) or (not practice):
            error = True
            reason = '评价内容所有项均不得为空'
        else:
            record = _TeacherRecord(
                teacher=teacher,
                school=int(school),
                grade=int(grade),
                course=int(course),
                book=int(book),
                unit=int(unit),
                note=note,
                study=int(study),
                knowledge=int(knowledge),
                practice=int(practice),
                study_note=study_note,
                date=date
            )
            record.save()

    return render(request, 'teacherrecordpage.html', {
        'user': user_info(request),
        'teacher': teacher,
        'records': records,

        'post': post,
        'error': error,
        'reason': reason,

        'school_choices': _TeacherRecord.SCHOOL_CHOICES,
        'grade_choices': _TeacherRecord.GRADE_CHOICES,
        'course_choices': _TeacherRecord.COURSE_CHOICES,
        'book_choices': _TeacherRecord.BOOK_CHOICES,
        'unit_choices': _TeacherRecord.UNIT_CHOICES,
        'study_choices': _TeacherRecord.STUDY_CHOICES,
        'knowledge_choices': _TeacherRecord.KNOWLEDGE_CHOICES,
        'practice_choices': _TeacherRecord.PRACTICE_CHOICES
    })


def edit_teacher_record(request, rid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _TeacherRecord.objects.filter(id=int(rid)):
        return HttpResponse('没有找到对应记录')

    record = _TeacherRecord.objects.filter(id=int(rid)).first()
    teacher = record.teacher

    post = False
    error = False
    reason = None

    if request.method == 'POST':
        post = True
        data = request.POST

        school = data.get('school')
        grade = data.get('grade')
        course = data.get('course')
        book = data.get('book')
        unit = data.get('unit')
        study = data.get('study')
        knowledge = data.get('knowledge')
        practice = data.get('practice')
        note = data.get('note')
        study_note = data.get('study_note')
        date = data.get('date')

        if (not school) or (not grade) or (not course) or (not book) or (not unit) or (not date):
            error = True
            reason = '学习内容所有项均不得为空'
        elif (not study) or (not knowledge) or (not practice):
            error = True
            reason = '评价内容所有项均不得为空'
        else:
            record.school = int(school)
            record.grade = int(grade)
            record.course = int(course)
            record.book = int(book)
            record.unit = int(unit)
            record.note = note
            record.study = int(study)
            record.knowledge = int(knowledge)
            record.practice = int(practice)
            record.study_note = study_note
            record.date = date
            record.save()
            print(record)
            print(record.unit)

    record = _TeacherRecord.objects.filter(id=int(rid)).first()

    return render(request, 'editteacherrecord.html', {
        'user': user_info(request),
        'teacher': teacher,
        'record': record,

        'post': post,
        'error': error,
        'reason': reason,

        'school_choices': _Record.SCHOOL_CHOICES,
        'grade_choices': _Record.GRADE_CHOICES,
        'course_choices': _Record.COURSE_CHOICES,
        'book_choices': _Record.BOOK_CHOICES,
        'unit_choices': _Record.UNIT_CHOICES,
        'study_choices': _Record.STUDY_CHOICES,
        'knowledge_choices': _Record.KNOWLEDGE_CHOICES,
        'practice_choices': _Record.PRACTICE_CHOICES
    })


def delete_teacher_record(request, rid):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not _Admin.objects.filter(user=request.user).exists():
        return redirect('/')
    elif not _TeacherRecord.objects.filter(id=int(rid)):
        return HttpResponse('没有找到对应记录')

    record = _TeacherRecord.objects.filter(id=int(rid)).first()
    teacher = record.teacher
    record.delete()

    return redirect('/teacher-record/' + str(teacher.id) + '/')