from django.db import models
from django.contrib.auth.models import AbstractUser
import re
import time
import random
import string
from connecter.fetcher import fetch
from connecter.executor import execute_solution as execute_solution_on_db


class StudentGroup(models.Model):
    title = models.CharField(max_length=255)
    #courses = models.ManyToManyField(Course)
    #owner = models.ForeignKey(User, related_name="created_groups", on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class User(AbstractUser):

    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True)
    group_number = models.ForeignKey(StudentGroup, on_delete=models.PROTECT, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role', 'tel', 'group_number']

    def __str__(self):
        return self.username


def database_src_path(instance, filename):
    return 'sandbox_db_{0}/src/{1}'.format(instance.id, filename)


def database_media_path(instance, filename):
    return 'sandbox_db_{0}/media/{1}'.format(instance.id, filename)


class Database(models.Model):
    owner = models.ForeignKey(
        User, related_name='databases', on_delete=models.PROTECT)
    title = models.CharField(max_length=512)

    description = models.TextField(max_length=8192)
    source_code = models.TextField(max_length=65535, null=True, blank=True)
    source_file = models.FileField(
        upload_to=database_src_path,
        null=True,
        blank=True
    )

    def get_sql(self):
        sql = None
        if self.source_code != None and self.source_code.strip() != '':
            sql = self.source_code
        else:
            sql = self.source_file.read().decode('utf-8')

        sql = sql.replace('\r', '')
        sql = re.sub(r'(\/\*(.|\n)*\*\/)|(--.*(\n|$))', '', sql)
        print('get_sql', sql)
        return sql

    def get_db_name(self):
        sql = self.get_sql().lower()
        #print('get_db_name - первый этап', sql)
        db_names = re.findall(r'(?<=create database )[a-zA-Z0-9_-]+(?=;)', sql)
        print('Имя используемой БД', db_names)
        #print('get_db_name - db_names', db_names),
        if len(db_names) > 0:
            return db_names[0]
        return None

    def init_db(self):
        db_name = self.get_db_name()
        print('init_db', db_name)
        if db_name:
            db_name_unique = db_name + \
                ''.join(random.choices(string.ascii_lowercase, k=5))
            #print('db_name_unique', db_name_unique)
            #print('exec', self.get_sql().replace(db_name, db_name_unique))
            success, data, error = fetch(
                self.get_sql().replace(db_name, db_name_unique))
            print('новое имя бд', db_name_unique)
            print('success, data, error', success, data, error)
            # if success:
            return db_name_unique

    def drop_db(self, name=None):
        if not name:
            name = self.get_db_name()

        if self.get_db_name() in name:
            fetch('drop database {};'.format(name))

    def execute_solution(self, solution_sql):

        db_name = self.init_db()
        print('execute_solution', db_name)
        t_start = time.time()
        try:
            for i in range(1):
                #print("этап вызова экзекутора", db_name, solution_sql)
                data = execute_solution_on_db(db_name, solution_sql)
            t_finish = time.time()

        except Exception as e:
            #print('exception', e)
            raise e
        finally:
            print('finally')
            # self.drop_db(db_name)

        return (data, t_finish - t_start)


class DatabaseImage(models.Model):
    database = models.ForeignKey(
        Database, related_name='images', on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to=database_media_path,
        null=True,
        blank=True
    )


class Task(models.Model):
    EASIER = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    HARDER = 5
    DIFFICULTY = (
        (EASIER, 'Очень просто'),
        (EASY, 'Легко'),
        (MEDIUM, 'Средний уровень'),
        (HARD, 'Трудно'),
        (HARDER, 'Очень сложно')
    )

    title = models.CharField(max_length=512)
    task_text = models.TextField(max_length=4096)
    reference_solution = models.TextField(max_length=8192)
    sandbox_db = models.ForeignKey(
        Database, related_name='tasks', on_delete=models.PROTECT)
    owner = models.ForeignKey(
        User, related_name='tasks', on_delete=models.PROTECT)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=MEDIUM)
    banned_words = models.TextField(max_length=2048, null=True)
    required_words = models.TextField(max_length=2048, null=True)
    number_of_attempts = models.IntegerField(default=10)
    should_check_runtime = models.BooleanField(default=False)
    allowed_time_error = models.FloatField(default=0.0)

    def execute_solution(self, sql_solution, attempts_count):
        if attempts_count >= self.number_of_attempts:
            return (False, "Превышен лимит попыток прохождения задания")

        for w in self.banned_words.lower().replace(' ', '').split(','):
            if w in sql_solution.lower():
                return (False, "Решение не должно содержать в себе этих слов: {}".format(self.banned_words.upper()))

        for w in self.required_words.lower().replace(' ', '').split(','):
            if w not in sql_solution.lower():
                return (False, "Решение должно содержать в себе эти слова: {}".format(self.required_words.upper()))

        print('база, которую будем создавать',
              Database.objects.get(pk=self.sandbox_db.pk).title)
        ref_result, ref_time = self.sandbox_db.execute_solution(
            self.reference_solution)
        #
        student_result, student_time = self.sandbox_db.execute_solution(
            sql_solution)
        print('результаты в моделе', ref_result[1], student_result[1])
        # if self.should_check_runtime and (
        #         (student_time / 10) <= ((ref_time / 10) * (1 + self.allowed_time_error) / 100)):
        #     return (False, "Решение превысило допустимый порог времени исполнения ({}s)".format(
        #         str(ref_time + self.allowed_time_error)))

        return (ref_result, student_result)


class SetOfTask(models.Model):
    title = models.CharField(max_length=512)
    tasks = models.ManyToManyField(Task, through='IncludedTask', default=1)
    owner = models.ForeignKey(
        User, related_name='set_of_tasks', on_delete=models.PROTECT, default=1)
    status = models.CharField(max_length=100)  # TODO: make it selectable


class IncludedTask(models.Model):
    setoftask = models.ForeignKey(SetOfTask, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Theme(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(max_length=8192)
    sets_of_task = models.ManyToManyField(SetOfTask, null=True)
    owner = models.ForeignKey(
        User, related_name='themes', on_delete=models.PROTECT)


class TaskInTheme(models.Model):
    task = models.ForeignKey(Task, related_name='themes',
                             on_delete=models.PROTECT, null=True)
    theme = models.ForeignKey(
        Theme, related_name='tasks', on_delete=models.PROTECT, null=True)
    affilation = models.FloatField()


class Course(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(max_length=8192)
    themes = models.ManyToManyField(Theme)
    owner = models.ForeignKey(
        User, related_name='courses', on_delete=models.PROTECT)


# class TaskResult(models.Model):
#     set_of_task = models.ForeignKey(SetOfTask, on_delete=models.PROTECT)
#     task = models.ForeignKey(Task, on_delete=models.PROTECT)


class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    account = models.ForeignKey(User, on_delete=models.PROTECT)
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(null=True)
    access_course = models.CharField(max_length=100)


class UserMasteringTheme(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)
    user_course = models.ForeignKey(UserCourse, on_delete=models.PROTECT)
    degree_of_mastering = models.FloatField()


class UserPriorityTheme(models.Model):
    """В текущей версии не используется"""
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)
    priority = models.FloatField()
    user_course = models.ForeignKey(UserCourse, on_delete=models.PROTECT)


class IndividualRouteStep(models.Model):
    """Результат выполнения студентом задания, состоящего в комплекте заданий, который состоит в курсе"""
    status = models.CharField(
        max_length=100, null=True)  # TODO: make it selectable
    user_course = models.ForeignKey(
        UserCourse, on_delete=models.PROTECT, null=True)
    task_in_set = models.ForeignKey(
        IncludedTask, on_delete=models.PROTECT, default=1, null=True)
    solution = models.TextField(max_length=8192, null=True)
    next_step = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT)


# class Membership(models.Model):
#     person = models.ForeignKey(User, on_delete=models.CASCADE)
#     group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
#     date_joined = models.DateField()
#     invite_reason = models.CharField(max_length=64)

# class ResultTask(models.Model):
#     """Результат выполнения студентом задания, состоящего в комплекте заданий, который состоит в курсе"""
