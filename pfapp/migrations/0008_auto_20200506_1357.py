# Generated by Django 3.0.3 on 2020-05-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfapp', '0007_auto_20200425_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='phoneno',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='user_locations',
            name='country',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user_locations',
            name='district',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user_locations',
            name='locality',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user_locations',
            name='state',
            field=models.CharField(max_length=30),
        ),
    ]
