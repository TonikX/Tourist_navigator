from django.db import models
from django.contrib.auth.models import AbstractUser


class TouristClass(models.Model):
    class_name = models.TextField()
    class_description = models.TextField()

    def __str__(self):
        return self.class_name


class User(AbstractUser):
    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True)
    user_class = models.ManyToManyField(TouristClass)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role', 'tel']

    def __str__(self):
        return self.username


class ObjType(models.Model):
    type_name = models.TextField()
    REQUIRED_FIELDS = ['type_name']

    def __str__(self):
        return self.type_name


class MapObject(models.Model):
    name=models.TextField()
    image_link=models.TextField(blank=True, null=True)
    geo_coordinates = models.TextField()
    description = models.TextField()
    object_type = models.ManyToManyField(ObjType, blank=True, null=True)
    full_address = models.TextField(blank=True, null=True)
    REQUIRED_FIELDS = ['keywords', 'coordinates', 'object_type']

    def __str__(self):
        return self.description


class AuthorRoute(models.Model):
    description = models.TextField()
    route_author = models.ForeignKey(User, related_name="author_id", on_delete=models.CASCADE)
    map_object = models.ManyToManyField(MapObject, through='AuthorRouteComposition')
    REQUIRED_FIELDS = ['route_author', 'map_object']

    def __str__(self):
        return self.description


class AuthorRouteComposition(models.Model):
    map_id = models.ForeignKey(MapObject, related_name="id_map_obj", on_delete=models.CASCADE)
    route_id = models.ForeignKey(AuthorRoute, related_name="route_id", on_delete=models.CASCADE)
    obj_position = models.IntegerField()
    REQUIRED_FIELDS = ['map_id', 'route_id', 'obj_position']

    def __str__(self):
        return self.route_id.description


class IndividualRoute(models.Model):
    route_user = models.ForeignKey(User, related_name="route_user_id", on_delete=models.CASCADE)
    obj_map = models.ManyToManyField(MapObject, through='RouteComposition')
    comment = models.TextField()
    REQUIRED_FIELDS = ['route_user', 'obj_map']


class RouteComposition(models.Model):
    map_id = models.ForeignKey(MapObject, on_delete=models.CASCADE)
    route_id = models.ForeignKey(IndividualRoute, on_delete=models.CASCADE)
    obj_position = models.IntegerField()
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    REQUIRED_FIELDS = ['map_id', 'route_id', 'obj_position']
