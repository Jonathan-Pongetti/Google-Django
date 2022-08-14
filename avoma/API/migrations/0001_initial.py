# Generated by Django 4.0.4 on 2022-07-31 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('Id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('StartTime', models.CharField(default='', max_length=50, null=True)),
                ('EndTime', models.CharField(default='', max_length=50, null=True)),
                ('Duration', models.TimeField(null=True)),
                ('Creator', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
    ]