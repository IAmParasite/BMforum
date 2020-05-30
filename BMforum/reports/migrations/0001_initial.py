# Generated by Django 2.2.3 on 2020-05-29 09:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='标题')),
                ('text', models.TextField(verbose_name='举报原因')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.Comment', verbose_name='评论')),
            ],
            options={
                'verbose_name': '举报',
                'verbose_name_plural': '举报',
            },
        ),
    ]