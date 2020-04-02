from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .serializers import DatabaseSerializer, StudentGroupSerializer, TaskSerializer, TaskInThemeSerializer, SetOfTaskSerializer, ThemeSerializer, CourseSerializer, UserCourseSerializer, UserCourseSetInitialsSerializer, UserCourseDoTaskSerializer, IndividualRouteStepSerializer
from .models import Database, StudentGroup, Task, TaskInTheme, SetOfTask, Theme, Course, UserCourse, IndividualRouteStep
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from AirsoftKit.permissions import IsStudent
from rest_framework.exceptions import APIException
from rest_framework import generics
from django.shortcuts import get_list_or_404
from connecter.fetcher import fetch
from django.http import Http404
from django.shortcuts import redirect


User = get_user_model()


class ListUser(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"User": serializer.data})


class StudentGroupView(generics.ListCreateAPIView):
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return StudentGroup.objects.all()


class DatabaseListCreateView(generics.ListCreateAPIView):
    """Контроллер для работы со списком баз данных, при создании бд.
    В минимально жизнеспособном продукте функции возложены на ДжангоАдмин"""

    serializer_class = DatabaseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return user.databases.all()

    def perform_create(self, serializer):
        sql_code = None

        if serializer.validated_data['source_code']:
            sql_code = str(serializer.validated_data['source_code'])
        else:
            try:
                sql_code = str(
                    serializer.validated_data['source_file'].read().decode('utf-8'))
            except Exception as e:
                raise APIException({'source_file': e})

        success, data, error = fetch(sql_code)
        if (success):
            instance = serializer.save(owner=self.request.user)
            instance.drop_db()

        else:
            raise APIException({'stacktrace': data})


class DatabaseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Апдейт учебной БД по номеру. В минимально жизнеспособном продукте функции возложены на ДжангоАдмин"""
    serializer_class = DatabaseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return user.databases.all()


class DatabaseRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    """Удаление учебной БД по номеру. В минимально жизнеспособном продукте функции возложены на ДжангоАдмин"""
    serializer_class = DatabaseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return user.databases.all()


class DatabaseRetrieveView(generics.RetrieveAPIView):
    """Получение одной базы данных по номеру"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes = [permissions.AllowAny, ]


class TaskListCreateView(generics.ListCreateAPIView):
    """Контроллер для работы со списком заданий, которые разработал пользователь.
       В минимально жизнеспособном продукте функции возложены на ДжангоАдмин"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        print(self.request.user)
        user = self.request.user
        return user.tasks.all()

    def perform_create(self, serializer):
        if serializer.validated_data['sandbox_db'].owner != self.request.user:
            raise generics.ValidationError('Вы можете прикреплять к заданиям '
                                           'только свои базы данных')
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Контроллер для обновления.
       В минимально жизнеспособном продукте функции возложены на ДжангоАдмин"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()

    def perform_update(self, serializer):
        if serializer.validated_data['sandbox_db'].owner != self.request.user:
            raise generics.ValidationError('Вы можете прикреплять к заданиям '
                                           'только свои базы данных')
        serializer.save(owner=self.request.user)


class TaskRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    """Контроллер для удаление.
       В минимально жизнеспособном продукте функции возложены на ДжангоАдмин"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()


class TaskRetrieveView(generics.RetrieveAPIView):
    """Получение одного задания по номеру"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return Task.objects.all()


# TODO: Добавить проверку суммы == 1
class TaskInThemeListCreateView(generics.ListCreateAPIView):

    serializer_class = TaskInThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return TaskInTheme.objects.filter(task__owner=user)

    def perform_create(self, serializer):
        if serializer.validated_data['task'].owner != self.request.user != serializer.validated_data['theme'].owner:
            raise generics.ValidationError(
                'Вы можете управлять только вашими объектами')
        serializer.save()


# TODO: Добавить проверку суммы == 1
class TaskInThemeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskInThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return TaskInTheme.objects.filter(task__owner=user)

    def perform_update(self, serializer):
        if (serializer.validated_data['task'].owner != self.request.user or
                serializer.validated_data['theme'].owner != self.request.user):
            raise generics.ValidationError(
                'Вы можете управлять только вашими объектами')
        serializer.save()


class TaskInThemeRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = TaskInThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return TaskInTheme.objects.filter(task__owner=user)


class TaskInThemeRetrieveView(generics.RetrieveAPIView):
    serializer_class = TaskInThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return TaskInTheme.objects.filter(task__owner=user)


class SetOfTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = SetOfTaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return SetOfTask.objects.filter(owner=user)

    def perform_create(self, serializer):
        for task in serializer.validated_data['tasks']:
            if task.owner != self.request.user:
                raise generics.ValidationError('Вы можете прикреплять к комплектам '
                                               'только свои задания')

        if len(serializer.validated_data['tasks']) > 3:
            raise generics.ValidationError(
                'В комплект можно поместить не более трех заданий')

        serializer.save(owner=self.request.user)


class SetOfTaskRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SetOfTaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return SetOfTask.objects.filter(owner=user)

    def perform_update(self, serializer):
        for task in serializer.validated_data['tasks']:
            if task.owner != self.request.user:
                raise generics.ValidationError('Вы можете прикреплять к комплектам '
                                               'только свои задания')

        if len(serializer.validated_data['tasks']) > 3:
            raise generics.ValidationError(
                'В комплект можно поместить не более трех заданий')

        serializer.save(owner=self.request.user)


class SetOfTaskRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = SetOfTaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return SetOfTask.objects.filter(owner=user)


class SetOfTaskRetrieveView(generics.RetrieveAPIView):
    serializer_class = SetOfTaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return SetOfTask.objects.filter(owner=user)


class ThemeListCreateView(generics.ListCreateAPIView):
    serializer_class = ThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Theme.objects.filter(owner=user)

    def perform_create(self, serializer):
        for set_of_task in serializer.validated_data.get('sets_of_task', []):
            if set_of_task.owner != self.request.user:
                raise generics.ValidationError('Вы можете прикреплять к темам '
                                               'только свои комплекты')

        return serializer.save(owner=self.request.user)


class ThemeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Theme.objects.filter(owner=user)

    def perform_update(self, serializer):
        for set_of_task in serializer.validated_data['sets_of_task']:
            if set_of_task.owner != self.request.user:
                raise generics.ValidationError('Вы можете прикреплять к темам '
                                               'только свои комплекты')

        serializer.save(owner=self.request.user)


class ThemeRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = ThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Theme.objects.filter(owner=user)


class ThemeRetrieveView(generics.RetrieveAPIView):
    serializer_class = ThemeSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Theme.objects.filter(owner=user)


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        for theme in serializer.validated_data.get('themes', []):
            if theme.owner != self.request.user:
                raise generics.ValidationError('Вы можете прикреплять к курсам '
                                               'только свои темы')

        return serializer.save(owner=self.request.user)


class CourseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user)

    def perform_update(self, serializer):
        for theme in serializer.validated_data.get('themes', []):
            if theme.owner != self.request.user:
                raise generics.ValidationError('Вы можете прикреплять к курсам '
                                               'только свои темы')

        serializer.save(owner=self.request.user)


class CourseRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user)


class CourseRetrieveView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user)


class UserCourseListCreateView(generics.ListCreateAPIView):
    """Контроллер взятия и окончания курса учеником"""
    serializer_class = UserCourseSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        user = self.request.user
        return UserCourse.objects.filter(account=user)

    def perform_create(self, serializer):
        return serializer.save(
            course=serializer.validated_data.get('course'),
            account=self.request.user
        )


class UserCourseSetInitialsView(generics.CreateAPIView):
    """Нихуя не понимаю зачем это нужно, туду: сделать заново"""
    serializer_class = UserCourseSetInitialsSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        course = UserCourse.objects.get(pk=self.kwargs['pk'])

        # for i, pr in enumerate(serializer.validated_data['priority']):
        #     serializer.validated_data['priority'].user_course = course

        for i, ma in enumerate(serializer.validated_data['mastering']):
            serializer.validated_data['mastering'].user_course = course

        serializer.validated_data['course'] = course

        serializer.save(**serializer.validated_data)


class DoTask(APIView):
    """Модуль проверки выполненного студентомзадания. На вход получает номер task и sql-запрос студента"""
    serializer_class = UserCourseDoTaskSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_object(self, pk):
        try:
            return IndividualRouteStep.objects.get(pk=pk)
        except IndividualRouteStep.DoesNotExist:
            raise Http404

    def put(self, request,  *args, **kwargs):
        serializer = UserCourseDoTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.get(pk=self.kwargs['task_id'])
        #print('данные из сериалайзера в начале выполнения проверки', serializer)
        (ref_result, student_result) = task.execute_solution(
            serializer.validated_data['solution'], 1)
        print('результаты в контроллере',ref_result, student_result)

        if (ref_result[1] == student_result[1]):
            print ('results ravni')
            """Часть кода, отвячающая за сохранение информации об супешновыполненном задании. 
            Маршрут задан заранее в таблице IndividualRouteStep. 
            В случае верного выполнения задания, меняется значение поля status.
            ToDo: на данный момент значение поля ststus берется из запроса. Сделать через context"""
            IndividualRouteStep = self.get_object(request.data.get('id'))
            print (IndividualRouteStep,'IndividualRouteStep')
            serializer = IndividualRouteStepSerializer(
                IndividualRouteStep, data=request.data)
            print('next step', request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok', 'next_task': request.data.get('next_step')})
            else:
                return Response({'status': 'mistake'})

        else:
            print('не равны')
            if ref_result == False:
                raise generics.ValidationError(student_result)
            else:
                return Response({
                    'status': 'error',
                    'ref_result': ref_result,
                    'student_result': student_result
                })


class IndividualRoute(APIView):
    #serializer_class = IndividualRouteStepSerializer
    permission_classes = [permissions.AllowAny, ]

    # def get(self):
    #     try:
    #         return IndividualRouteStep.objects.get(pk=pk)
    #     except IndividualRouteStep.DoesNotExist:
    #         raise Http404

    def get_object(self, pk):
        try:
            return IndividualRouteStep.objects.get(pk=pk)
        except IndividualRouteStep.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        serializer = IndividualRouteStepSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid():
            serializer.is_valid()

            print(serializer)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response({'status': 'mistake'})

    def put(self, request, *args, **kwargs):
        #print('id изменяемой записи', request.data.get('id'))
        IndividualRouteStep = self.get_object(request.data.get('id'))
        serializer = IndividualRouteStepSerializer(
            IndividualRouteStep, data=request.data)
        print(request.data)

        if serializer.is_valid():
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'status': 'mistake'})


class CoursesListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return Course.objects.all()