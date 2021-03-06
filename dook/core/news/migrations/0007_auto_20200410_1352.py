# Generated by Django 3.0.4 on 2020-04-10 13:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20200406_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensitiveKeyword',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='news',
            name='is_sensitive',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='NewsSensitiveKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News')),
                ('sensitive_keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newssensitivekeyword_set', to='news.SensitiveKeyword')),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='sensitive_keywords',
            field=models.ManyToManyField(through='news.NewsSensitiveKeyword', to='news.SensitiveKeyword'),
        ),
    ]
