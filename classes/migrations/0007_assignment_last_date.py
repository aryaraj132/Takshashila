# Generated by Django 2.2 on 2021-02-15 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_auto_20210216_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='last_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
