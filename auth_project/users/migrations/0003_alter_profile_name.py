# Generated by Django 4.2.22 on 2025-06-06 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_menuitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(choices=[{'admin', 'Adminstrador'}, {'anfitriao', 'Anfitrião'}, {'Convidado', 'guest'}], max_length=50, unique=True),
        ),
    ]
