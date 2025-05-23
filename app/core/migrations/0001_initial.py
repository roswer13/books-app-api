# Generated by Django 5.2.1 on 2025-05-10 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(help_text='Email address of the user.', max_length=128, unique=True, verbose_name='Email')),
                ('name', models.CharField(help_text='Name of the user.', max_length=128, verbose_name='User name')),
                ('role', models.CharField(choices=[('editor', 'Editor'), ('reader', 'Reader')], default='reader', help_text='Role of the user.', max_length=16, verbose_name='User role')),
                ('is_staff', models.BooleanField(default=False, help_text='Is a user of the internal equipment.', verbose_name='Staff')),
                ('is_active', models.BooleanField(default=True, help_text='Indicates if the user is active.', verbose_name='Active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
