from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    # 学生
    TYPE_CHOICES = (
        (1, '一对一教学'),
        (2, '自习'),
        (3, '一对一 + 自习'),
    )
    name = models.CharField(max_length=32)
    type = models.IntegerField(choices=TYPE_CHOICES)

    tutor = models.ForeignKey(to='Tutor', related_name='student')               # 所属班主任


class Teacher(models.Model):
    # 教师
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    time = models.IntegerField(default=0)

    course = models.ManyToManyField(to='Course', related_name='teacher')             # 教授科目


class Tutor(models.Model):
    # 班主任
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

    user = models.OneToOneField(to=User, related_name='tutor')  # 绑定的账号


class Admin(models.Model):
    # 管理员
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

    user = models.OneToOneField(to=User, related_name='admin')  # 绑定的账号


class Course(models.Model):
    # 科目
    name = models.CharField(max_length=128)
    index = models.CharField(max_length=16, unique=True)
    teacher_num = models.IntegerField(default=0)


class CourseSelect(models.Model):
    # 学生所选科目
    course = models.ForeignKey(Course, related_name='select')           # 所选科目
    student = models.ForeignKey(Student, related_name='select')         # 学生
    teacher = models.ForeignKey(Teacher, related_name='select')         # 老师
    time = models.IntegerField(default=0)                               # 剩余课时


class CommentType(models.Model):
    # 评价类型
    name = models.CharField(max_length=64, unique=True)


class Comment(models.Model):
    # 评价
    type = models.ForeignKey(to='CommentType', related_name='comment')
    content = models.TextField()
    score = models.IntegerField()


class ClassRecord(models.Model):
    # 上课记录
    SCHOOL_CHOICES = (
        (1, '小学'),
        (2, '初中'),
        (3, '高中'),
    )
    GRADE_CHOICES = (
        (1, '一年级'),
        (2, '二年级'),
        (3, '三年级'),
        (4, '四年级'),
        (5, '五年级'),
    )
    COURSE_CHOICES = (
        (1, '语文'),
        (2, '数学'),
        (3, '外语'),
        (4, '物理'),
        (5, '化学'),
        (6, '生物'),
    )
    BOOK_CHOICES = (
        (1, '上册'),
        (2, '下册'),
    )
    UNIT_CHOICES = (
        (1, '第一单元'),
        (2, '第二单元'),
        (3, '第三单元'),
        (4, '第四单元'),
        (5, '第五单元'),
        (6, '第六单元'),
        (7, '第七单元'),
        (8, '第八单元'),
        (9, '第九单元'),
    )

    STUDY_CHOICES = (
        (1, '学习状态：学习状态不佳，注意力无法集中'),
        (2, '学习状态：刚开始上课注意力较为集中，但无法维持良好的学习状态，注意力分散较快'),
        (3, '学习状态：刚开始上课注意力不集中，但稍后就有改善。'),
        (4, '学习状态：注意力较为集中，学习状态不错'),
    )
    KNOWLEDGE_CHOICES = (
        (1, '知识接受情况：知识接受情况较差，听不进去课'),
        (2, '知识接受情况：知识接受情况较差，可以接受，但不能理解'),
        (3, '知识接受情况：知识接受情况良好，讲到的内容都可以接受')
    )
    PRACTICE_CHOICES = (
        (1, '练习反馈：练习表现较差，知识未能消化，还需要对知识点进行巩固复习和多加练习'),
        (2, '练习反馈：练习状况良好，但并未能完全掌握所学的内容，需要多加练习'),
        (3, '练习反馈：练习完成情况不错，能熟练的运用学到的知识'),
    )

    student = models.ForeignKey(to=Student, related_name='record')
    school = models.IntegerField(choices=SCHOOL_CHOICES)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    course = models.IntegerField(choices=COURSE_CHOICES)
    book = models.IntegerField(choices=BOOK_CHOICES)
    unit = models.IntegerField(choices=UNIT_CHOICES)
    note = models.TextField(null=True)

    study = models.IntegerField(choices=STUDY_CHOICES)
    knowledge = models.IntegerField(choices=KNOWLEDGE_CHOICES)
    practice = models.IntegerField(choices=PRACTICE_CHOICES)
    study_note = models.TextField(null=True)

    date = models.DateField()


class TeacherRecord(models.Model):
    # 上课记录
    SCHOOL_CHOICES = (
        (1, '小学'),
        (2, '初中'),
        (3, '高中'),
    )
    GRADE_CHOICES = (
        (1, '一年级'),
        (2, '二年级'),
        (3, '三年级'),
        (4, '四年级'),
        (5, '五年级'),
    )
    COURSE_CHOICES = (
        (1, '语文'),
        (2, '数学'),
        (3, '外语'),
        (4, '物理'),
        (5, '化学'),
        (6, '生物'),
    )
    BOOK_CHOICES = (
        (1, '上册'),
        (2, '下册'),
    )
    UNIT_CHOICES = (
        (1, '第一单元'),
        (2, '第二单元'),
        (3, '第三单元'),
        (4, '第四单元'),
        (5, '第五单元'),
        (6, '第六单元'),
        (7, '第七单元'),
        (8, '第八单元'),
        (9, '第九单元'),
    )

    STUDY_CHOICES = (
        (1, '学习状态：学习状态不佳，注意力无法集中'),
        (2, '学习状态：刚开始上课注意力较为集中，但无法维持良好的学习状态，注意力分散较快'),
        (3, '学习状态：刚开始上课注意力不集中，但稍后就有改善。'),
        (4, '学习状态：注意力较为集中，学习状态不错'),
    )
    KNOWLEDGE_CHOICES = (
        (1, '知识接受情况：知识接受情况较差，听不进去课'),
        (2, '知识接受情况：知识接受情况较差，可以接受，但不能理解'),
        (3, '知识接受情况：知识接受情况良好，讲到的内容都可以接受')
    )
    PRACTICE_CHOICES = (
        (1, '练习反馈：练习表现较差，知识未能消化，还需要对知识点进行巩固复习和多加练习'),
        (2, '练习反馈：练习状况良好，但并未能完全掌握所学的内容，需要多加练习'),
        (3, '练习反馈：练习完成情况不错，能熟练的运用学到的知识'),
    )

    teacher = models.ForeignKey(to=Teacher, related_name='record')
    school = models.IntegerField(choices=SCHOOL_CHOICES)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    course = models.IntegerField(choices=COURSE_CHOICES)
    book = models.IntegerField(choices=BOOK_CHOICES)
    unit = models.IntegerField(choices=UNIT_CHOICES)
    note = models.TextField(null=True)

    study = models.IntegerField(choices=STUDY_CHOICES)
    knowledge = models.IntegerField(choices=KNOWLEDGE_CHOICES)
    practice = models.IntegerField(choices=PRACTICE_CHOICES)
    study_note = models.TextField(null=True)

    date = models.DateField()
