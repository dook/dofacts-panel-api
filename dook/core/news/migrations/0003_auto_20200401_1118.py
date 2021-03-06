# Generated by Django 3.0.4 on 2020-04-01 11:18from django.db import migrations, models
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):    
    dependencies = [
        ('news', '0002_news_created_at'),
    ]    
    operations = [
        migrations.RemoveField(
            model_name='expertopinion',
            name='duplicate_url',
        ),
        migrations.RemoveField(
            model_name='factcheckeropinion',
            name='duplicate_url',
        ),
        migrations.AddField(
            model_name='expertopinion',
            name='duplicate_reference',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='factcheckeropinion',
            name='duplicate_reference',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='expertopinion',
            name='news',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='news.News'),
        ),
    ]