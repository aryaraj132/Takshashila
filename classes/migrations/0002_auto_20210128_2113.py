# Generated by Django 2.2 on 2021-01-28 15:43

import classes.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_id', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=250)),
                ('position', models.PositiveSmallIntegerField(verbose_name='Lecture Number')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=classes.models.lesson_files, verbose_name='Video')),
                ('notes', models.FileField(blank=True, null=True, upload_to=classes.models.lesson_files, verbose_name='Notes')),
                ('ppt', models.FileField(blank=True, null=True, upload_to=classes.models.lesson_files, verbose_name='Presentation')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to=classes.models.subject_image, verbose_name='Subject Image')),
            ],
        ),
        migrations.RemoveField(
            model_name='subject',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='year',
        ),
        migrations.RemoveField(
            model_name='year',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='description',
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.DeleteModel(
            name='Year',
        ),
        migrations.AddField(
            model_name='subjects',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Branch'),
        ),
        migrations.AddField(
            model_name='subjects',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='classes.Semester'),
        ),
        migrations.AddField(
            model_name='semester',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester', to='classes.Branch'),
        ),
        migrations.AddField(
            model_name='lessons',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Branch'),
        ),
        migrations.AddField(
            model_name='lessons',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lessons',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Semester'),
        ),
        migrations.AddField(
            model_name='lessons',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='classes.Subjects'),
        ),
    ]
