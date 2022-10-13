# Generated by Django 3.1 on 2022-09-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_variation'),
        ('bookloan', '0003_auto_20220918_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookloanbook',
            name='variation',
        ),
        migrations.AddField(
            model_name='bookloanbook',
            name='variations',
            field=models.ManyToManyField(blank=True, to='bookstore.Variation'),
        ),
    ]