# Generated by Django 2.2 on 2021-02-15 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0013_auto_20210216_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='last_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]