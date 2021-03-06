# Generated by Django 2.2.6 on 2020-04-11 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tourist_app', '0003_auto_20200405_1531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mapobject',
            old_name='coordinates',
            new_name='geo_coordinates',
        ),
        migrations.RenameField(
            model_name='mapobject',
            old_name='keywords',
            new_name='name',
        ),
        migrations.AddField(
            model_name='mapobject',
            name='full_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mapobject',
            name='image_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mapobject',
            name='object_type',
            field=models.ManyToManyField(blank=True, null=True, to='Tourist_app.ObjType'),
        ),
    ]
