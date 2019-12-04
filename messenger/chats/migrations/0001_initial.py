# Generated by Django 2.2.5 on 2019-12-04 18:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('tag', models.CharField(max_length=50, unique=True, verbose_name='Тег для поиска')),
                ('is_group', models.BooleanField(default=False, verbose_name='Является ли чат группой')),
                ('is_channel', models.BooleanField(default=False, verbose_name='Является ли чат каналом')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Описание чата')),
                ('last_message', models.TextField(blank=True, null=True, verbose_name='Последнее сообщение в чате')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True, verbose_name='Содержание')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Время отправки')),
                ('type', models.CharField(default='text', max_length=15, verbose_name='Тип сообщения')),
                ('url', models.URLField(null=True, verbose_name='Ссылка на фото')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Chat', verbose_name='Чат')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-time'],
            },
        ),
    ]
