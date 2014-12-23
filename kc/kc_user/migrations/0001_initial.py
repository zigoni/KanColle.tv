# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
import re
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KcUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(max_length=254, unique=True, help_text='电子邮件必须真实有效，否则将无法激活账号', verbose_name='电子邮件')),
                ('username', models.CharField(db_index=True, unique=True, help_text='用户昵称可由英文字母、数字、汉字或假名组成，长度不超过20', verbose_name='用户昵称', max_length=20, validators=[django.core.validators.RegexValidator(re.compile('^[\\w\\d⺀-\u9fff]{2,}$', 32), '请输入至少两个字母、数字、汉字或假名', 'invalid')])),
                ('is_active', models.BooleanField(verbose_name='用户是否可用', default=True)),
                ('is_staff', models.BooleanField(verbose_name='是否为管理用户', default=False)),
                ('create_time', models.DateTimeField(verbose_name='用户创建时间', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', to='auth.Group', blank=True, related_query_name='user')),
            ],
            options={
                'verbose_name_plural': '用户',
                'verbose_name': '用户',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KcGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('symbol', models.CharField(max_length=20, unique=True, help_text='用于系统内部识别的标志，必须以英文字母开头，之后可有英文字母、数字或下划线，长度不超过20', verbose_name='标志', validators=[django.core.validators.RegexValidator(re.compile('^[\\w][\\w\\d_]{0,19}$', 32), '请按格式输入', 'invalid')])),
                ('name', models.CharField(max_length=20, unique=True, help_text='用于显示的名称，可使用任意字符，HTML标记无效，长度不超过20', verbose_name='名称')),
                ('description', models.CharField(max_length=200, help_text='对用户组的描述，可使用任意字符，HTML标记无效，长度不超过200', verbose_name='描述')),
            ],
            options={
                'verbose_name_plural': '用户组',
                'verbose_name': '用户组',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KcUserEmailConfirmation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=32, verbose_name='电子邮件确认代码')),
                ('create_time', models.DateTimeField(verbose_name='电子邮件确认请求创建时间', default=django.utils.timezone.now)),
                ('user', models.OneToOneField(related_name='email_confirmation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '电子邮件确认请求',
                'verbose_name': '电子邮件确认请求',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KcUserPasswordReset',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=32, verbose_name='密码重置代码')),
                ('create_time', models.DateTimeField(verbose_name='密码重置请求创建时间', default=django.utils.timezone.now)),
                ('user', models.OneToOneField(related_name='password_reset', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '密码重置请求',
                'verbose_name': '密码重置请求',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kcuser',
            name='kc_groups',
            field=models.ManyToManyField(blank=True, verbose_name='所属用户组', to='kc_user.KcGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kcuser',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission', blank=True, related_query_name='user'),
            preserve_default=True,
        ),
    ]
