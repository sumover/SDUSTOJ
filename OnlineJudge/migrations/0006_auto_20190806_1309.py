# Generated by Django 2.2.4 on 2019-08-06 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineJudge', '0005_contest_contestname'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='memoryLimit',
            field=models.IntegerField(default=128),
        ),
        migrations.AddField(
            model_name='problem',
            name='outputLimit',
            field=models.IntegerField(blank=True, default=4096),
        ),
        migrations.AddField(
            model_name='problem',
            name='timeLimit',
            field=models.DecimalField(decimal_places=9, default=1.0, max_digits=32),
            preserve_default=False,
        ),
    ]
