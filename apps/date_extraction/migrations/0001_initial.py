# Generated by Django 4.0.4 on 2022-07-07 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateExtraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docname', models.CharField(max_length=500)),
                ('docsentence', models.TextField()),
                ('datelabel', models.CharField(max_length=10)),
                ('isodate', models.CharField(max_length=10)),
            ],
        ),
    ]
