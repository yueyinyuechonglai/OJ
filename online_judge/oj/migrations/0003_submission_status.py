# Generated by Django 2.2.7 on 2019-12-20 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0002_remove_submission_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(default='Accepted', max_length=20),
            preserve_default=False,
        ),
    ]
