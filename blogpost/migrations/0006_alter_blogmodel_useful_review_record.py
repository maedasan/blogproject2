# Generated by Django 3.2.8 on 2021-11-16 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0005_auto_20211116_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='useful_review_record',
            field=models.TextField(null=True),
        ),
    ]
