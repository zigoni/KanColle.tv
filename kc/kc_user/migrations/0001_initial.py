# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KcUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(help_text='电子邮件必须真实有效，否则将无法激活账号', verbose_name='电子邮件', max_length=254, unique=True)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w\\d⺀-\u9fff]{2,}$', 32), '请输入至少两个字母、数字、汉字或假名', 'invalid')], help_text='用户昵称可由英文字母、数字、汉字或假名组成，长度不超过20', verbose_name='用户昵称', max_length=20, db_index=True, unique=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='用户是否可用')),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否为管理用户')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='用户创建时间')),
                ('groups', models.ManyToManyField(related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', related_query_name='user', to='auth.Group', blank=True)),
            ],
            options={
                'verbose_name': 'KTV用户',
                'verbose_name_plural': 'KTV用户',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KcGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('symbol', models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w][\\w\\d_]{0,19}$', 32), '请按格式输入', 'invalid')], help_text='用于系统内部识别的标志，必须以英文字母开头，之后可有英文字母、数字或下划线，长度不超过20', verbose_name='标志', max_length=20, unique=True)),
                ('name', models.CharField(help_text='用于显示的名称，可使用任意字符，HTML标记无效，长度不超过20', verbose_name='名称', max_length=20, unique=True)),
                ('description', models.CharField(help_text='对用户组的描述，可使用任意字符，HTML标记无效，长度不超过200', verbose_name='描述', max_length=200)),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KcUserEmailConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(verbose_name='电子邮件确认代码', max_length=32)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='电子邮件确认请求创建时间')),
                ('user', models.OneToOneField(related_name='email_confirmation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '电子邮件确认请求',
                'verbose_name_plural': '电子邮件确认请求',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KcUserPasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(verbose_name='密码重置代码', max_length=32)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='密码重置请求创建时间')),
                ('user', models.OneToOneField(related_name='password_reset', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '密码重置请求',
                'verbose_name_plural': '密码重置请求',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kcuser',
            name='kc_groups',
            field=models.ManyToManyField(to='kc_user.KcGroup', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kcuser',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', help_text='Specific permissions for this user.', verbose_name='user permissions', related_query_name='user', to='auth.Permission', blank=True),
            preserve_default=True,
        ),
    ]
