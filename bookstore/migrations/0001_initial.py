# Generated by Django 3.1 on 2022-08-14 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genre', '0002_auto_20220815_0322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('author_name', models.CharField(blank=True, max_length=200)),
                ('publisher_name', models.CharField(blank=True, max_length=200)),
                ('Images', models.ImageField(upload_to='photos/books')),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genre.genre')),
            ],
        ),
    ]
