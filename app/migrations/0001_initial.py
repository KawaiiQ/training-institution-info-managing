# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-05 03:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CommentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('type', models.IntegerField(choices=[(1, 'One to One'), (2, 'Self-study'), (3, 'Both')])),
                ('time', models.IntegerField()),
                ('course', models.ManyToManyField(related_name='student', to='app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=32)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('comment', models.ManyToManyField(related_name='training', to='app.Comment')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training', to='app.Course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training', to='app.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='app.Tutor'),
        ),
        migrations.AddField(
            model_name='comment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='app.CommentType'),
        ),
    ]
