# Generated by Django 3.1.4 on 2020-12-19 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20201217_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='comment_id',
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.question'),
        ),
    ]
