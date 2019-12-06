# Generated by Django 2.2 on 2019-12-06 17:56

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('introduction', models.TextField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob_id', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=30)),
                ('time_lim', models.IntegerField()),
                ('mem_lim', models.IntegerField()),
                ('description', models.TextField()),
                ('input_format', models.TextField()),
                ('output_format', models.TextField()),
                ('example_inp', models.TextField()),
                ('exmaple_outp', models.TextField()),
                ('data_input', models.FileField(upload_to='')),
                ('data_output', models.FileField(upload_to='')),
            ],
        ),
    ]
