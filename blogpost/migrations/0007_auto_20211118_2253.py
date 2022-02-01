# Generated by Django 3.2.8 on 2021-11-18 13:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0006_alter_blogmodel_useful_review_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmodel',
            name='useful_comment',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='useful_review_record',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]