from rest_framework import serializers, viewsets

from .models import User, StudentGroup, Database, Task, SetOfTask, Theme, Course, TaskInTheme, UserMasteringTheme, UserPriorityTheme, UserCourse, IndividualRouteStep, IncludedTask


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        # fields = '__all__'
        fields = ("id", "title")


class userProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с акканутами"""
    user = serializers.StringRelatedField(read_only=True)
    #group_numbers = StudentGroupSerializer(source='group_number')

    class Meta:
        model = User
        fields = '__all__'
        #fields = ("first_name", "last_name", "email", "username", "group_numbers")
        #required_fields = fields


class UserSerializer(serializers.ModelSerializer):
    #group_numbers = StudentGroupSerializer(read_only=True, many=True)
    group_number = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='group_number'
    )
    class Meta:
        model = User
        # fields = '__all__'
        fields = ("id", "username", "first_name", "last_name", "email", "role", "status", "group_number")


class DatabaseSerializer(serializers.ModelSerializer):
    """Сериализатор для учебных баз данных"""
    class Meta:
        model = Database
        fields = ('id', 'title', 'description', 'source_code',
                  'source_file', 'images', 'owner', 'get_sql')
        read_only_fields = ('id', 'owner', 'get_sql')


class TaskInThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInTheme
        fields = ('id', 'task', 'theme', 'affilation')
        read_only_fields = ('id',)
        extra_kwargs = {'task': {'required': False}}

    def validate_affilation(self, attrs):
        try:
            affilation = float(attrs)
        except ValueError:
            raise serializers.ValidationError('Ожидалось число от 0 до 1')

        if affilation > 1 or affilation <= 0:
            raise serializers.ValidationError('Ожидалось число от 0 до 1')

        return attrs


class TaskSerializer(serializers.ModelSerializer):
    themes = TaskInThemeSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'task_text', 'difficulty', 'reference_solution',
                  'sandbox_db', 'owner', 'required_words',
                  'banned_words', 'should_check_runtime', 'number_of_attempts',
                  'allowed_time_error', 'themes')

        read_only_fields = ('id', 'owner')

    def create(self, validated_data):
        task_in_themes = validated_data.get('themes', [])
        task = Task(title=validated_data.get('title', None),
                    task_text=validated_data.get('task_text', None),
                    reference_solution=validated_data.get(
                        'reference_solution', None),
                    sandbox_db=validated_data.get('sandbox_db', None),
                    owner=validated_data.get('owner', None),
                    difficulty=validated_data.get('difficulty', None),
                    banned_words=validated_data.get('banned_words', None),
                    required_words=validated_data.get('required_words', None),
                    number_of_attempts=validated_data.get(
                        'number_of_attempts', None),
                    should_check_runtime=validated_data.get(
                        'should_check_runtime', None),
                    allowed_time_error=validated_data.get('allowed_time_error', None))
        task.save()

        for task_in_theme in task_in_themes:
            tit = TaskInTheme.objects.create(
                task=task,
                theme=task_in_theme['theme'],
                affilation=task_in_theme['affilation'])
            tit.save()

        return task

    def update(self, instance, validated_data):
        task_in_themes = validated_data.get('themes', [])

        instance.title = validated_data.get('title', instance.title)
        instance.task_text = validated_data.get(
            'task_text', instance.task_text)
        instance.reference_solution = validated_data.get(
            'reference_solution', instance.reference_solution)
        instance.sandbox_db = validated_data.get(
            'sandbox_db', instance.sandbox_db)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.difficulty = validated_data.get(
            'difficulty', instance.difficulty)
        instance.banned_words = validated_data.get(
            'banned_words', instance.banned_words)
        instance.required_words = validated_data.get(
            'required_words', instance.required_words)
        instance.number_of_attempts = validated_data.get(
            'number_of_attempts', instance.number_of_attempts)
        instance.should_check_runtime = validated_data.get(
            'should_check_runtime', instance.should_check_runtime)
        instance.allowed_time_error = validated_data.get(
            'allowed_time_error', instance.allowed_time_error)

        instance.save()

        for task_in_theme in task_in_themes:
            tit = TaskInTheme.objects.filter(
                task=instance,
                theme=task_in_theme['theme']
            ).update(affilation=task_in_theme['affilation'])

            if tit[0]:
                tit.affilation = task_in_theme['affilation']
            else:
                tit = TaskInTheme.objects.create(
                    task=task,
                    theme=task_in_theme['theme'],
                    affilation=task_in_theme['affilation'])

            tit.save()

        for old_tit in instance.themes.values():
            contains = False

            for t in task_in_themes:
                if t.task == old_tit.task and t.theme == old_tit.theme:
                    contains = True
                    break
            if not contains:
                TaskInTheme.objects.get(**old_tit).delete()

        return instance


class SetOfTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetOfTask
        fields = ('id', 'title', 'tasks', 'owner', 'status')
        read_only_fields = ('id', 'owner')


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'sets_of_task', 'owner')
        read_only_fields = ('id', 'owner')
        extra_kwargs = {'sets_of_task': {'required': False}}

    def create(self, validated_data):
        theme = Theme.objects.create(title=validated_data.get('title'),
                                     description=validated_data.get(
                                         'description'),
                                     owner=validated_data.get('owner'))

        for set_of_task in validated_data.get('sets_of_task', []):
            theme.sets_of_task.add(set_of_task)
        theme.save()

        return theme


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'themes', 'owner')
        read_only_fields = ('id', 'owner')


class UserCourseDoTaskSerializer(serializers.Serializer):
    task = serializers.IntegerField()
    solution = serializers.CharField(max_length=4096)
    #themes = TaskInThemeSerializer(many=True)

    # class Meta:
    #     model = IndividualRouteStep
    #     fields = ('id', 'status', 'user_course', 'task_in_set', 'solution')
    # status = serializers.CharField(max_length = 4096)
    # student_result = serializers.CharField(max_length = 4096)


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ('id', 'course', 'account', 'date_start',
                  'date_finish', 'access_course')
        read_only_fields = ('id', 'account', 'date_start',
                            'date_finish', 'access_course')


class IndividualRouteStepSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=8192)
    #user_course = serializers.PrimaryKeyRelatedField(many=True, queryset=UserCourse.objects.all())

    class Meta:
        model = IndividualRouteStep
        #fields = ('id', 'status', 'user_course', 'task_in_set', 'solution', 'next_step')
        fields = '__all__'

    def create(self, validated_data):
        irs = IndividualRouteStep(status=validated_data.get('status', None),
                                  user_course=validated_data.get(
                                      'user_course', None),
                                  task_in_set=validated_data.get(
                                      'task_in_set', None),
                                  solution=validated_data.get('solution', None))
        irs.save()

        return irs

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.user_course = validated_data.get(
            'user_course', instance.user_course)
        instance.task_in_set = validated_data.get(
            'title', instance.task_in_set)
        instance.solution = validated_data.get('title', instance.solution)
        instance.next_step = validated_data.get(
            'next_step', instance.next_step)
        instance.save()

        return instance
    # status = serializers.IntegerField()
    #solution = serializers.CharField(max_length=4096)
    # status = serializers.SerializerMethodField()
    #
    # def get_status(self, obj):
    #     if "status" in self.context:
    #         return self.context["status"]
    #     return None
    #
    # print('status', status)
    #
    # class Meta:
    #     model = IndividualRouteStep
    #     #fields = ('id', 'status', 'user_course', 'task_in_set', 'solution', 'next_step')
    #     fields = '__all__'
    print('d')
    # id = serializers.IntegerField(label='ID', read_only=True)
    # status = serializers.CharField(allow_null=True, max_length=100, required=False)
    # solution = serializers.CharField(allow_null=True, max_length=8192, required=False)
    # user_course = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=UserCourse.objects.all(), required=False)
    # task_in_set = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=IncludedTask.objects.all(), required=False)
    # next_step = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=IndividualRouteStep.objects.all(), required=False)
    #
    # def create(self, validated_data):
    #     IndividualRouteStep.save()
    #     return IndividualRouteStep.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.status = 1
    #     instance.solution = validated_data.get('solution', instance.solution)
    #     #instance.created = validated_data.get('created', instance.created)
    #     return instance


class UserMasteringThemeSerializer(serializers.ModelSerializer):
    """В моделе базы данных - UserMasteringTheme"""
    class Meta:
        model = UserMasteringTheme
        fields = ('id', 'theme', 'user_course', 'degree_of_mastering')
        read_only_fields = ('id',)


class UserPriorityThemeSerializer(serializers.ModelSerializer):
    """В текущей версии не используется"""
    class Meta:
        model = UserPriorityTheme
        fields = ('id', 'theme', 'user_course', 'priority')
        read_only_fields = ('id',)


class UserCourseSetInitialsSerializer(serializers.Serializer):
    course = UserCourseSerializer()
    #priority = UserPriorityThemeSerializer(many=True)
    mastering = UserMasteringThemeSerializer(many=True)
