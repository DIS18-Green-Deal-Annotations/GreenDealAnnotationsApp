# Generated by Django 3.1.13 on 2022-06-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('date_extraction', '0002_auto_20220618_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dateextraction',
            old_name='datelabel',
            new_name='DateLabel',
        ),
        migrations.RenameField(
            model_name='dateextraction',
            old_name='docsentence',
            new_name='DocSentence',
        ),
        migrations.RenameField(
            model_name='dateextraction',
            old_name='isodate',
            new_name='IsoDate',
        ),
        migrations.RemoveField(
            model_name='dateextraction',
            name='docname',
        ),
        migrations.AddField(
            model_name='dateextraction',
            name='DocName',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
