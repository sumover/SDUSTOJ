# Generated by Django 2.2.4 on 2019-08-08 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineJudge', '0008_auto_20190808_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submitfile',
            field=models.TextField(max_length=131072),
        ),
    ]