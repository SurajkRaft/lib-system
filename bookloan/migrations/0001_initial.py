# Generated by Django 3.1 on 2022-09-18 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstore', '0004_variation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookloan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookloan_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('bookloan_note', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Returned', 'Returned'), ('Cancelled', 'Cancelled')], default='New', max_length=15)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('is_bookloan', models.BooleanField(default=False)),
                ('return_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookloanBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edition', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('is_bookloan', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.book')),
                ('bookloan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookloan.bookloan')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.variation')),
            ],
        ),
    ]