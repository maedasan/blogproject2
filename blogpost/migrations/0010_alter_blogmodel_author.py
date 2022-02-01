# Generated by Django 3.2.8 on 2021-11-21 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogpost', '0009_alter_blogmodel_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
