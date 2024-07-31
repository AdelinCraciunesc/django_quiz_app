# Generated by Django 5.0.7 on 2024-07-30 22:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_user_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_result',
            name='score',
        ),
        migrations.AddField(
            model_name='question',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user_result',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quiz.category'),
        ),
    ]