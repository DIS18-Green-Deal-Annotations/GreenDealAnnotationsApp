# Generated by Django 3.1.13 on 2022-06-18 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('date_extraction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dateextraction',
            old_name='DateLabel',
            new_name='datelabel',
        ),
        migrations.RenameField(
            model_name='dateextraction',
            old_name='DocSentence',
            new_name='docsentence',
        ),
        migrations.RenameField(
            model_name='dateextraction',
            old_name='IsoDate',
            new_name='isodate',
        ),
        migrations.RemoveField(
            model_name='dateextraction',
            name='DocName',
        ),
        migrations.AddField(
            model_name='dateextraction',
            name='docname',
            field=models.CharField(default='null', max_length=500),
            preserve_default=False,
        ),
    ]
