# Generated by Django 4.1.3 on 2022-12-03 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('quantity_available', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now=True)),
                ('status', models.CharField(max_length=25)),
                ('quantity_issued', models.IntegerField(default=0)),
                ('return_date', models.DateField(null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_management.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_management.student')),
            ],
        ),
    ]
