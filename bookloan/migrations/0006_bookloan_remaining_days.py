# Generated by Django 3.1 on 2022-09-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookloan', '0005_auto_20220919_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookloan',
            name='remaining_days',
            field=models.IntegerField(default=False),
        ),
    ]
