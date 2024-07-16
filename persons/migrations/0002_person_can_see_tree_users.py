# Generated by Django 4.1.1 on 2024-07-16 10:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='can_see_tree_users',
            field=models.ManyToManyField(related_name='can_see_persons_tree', to=settings.AUTH_USER_MODEL, verbose_name='کاربرانی که می\u200cتوانند درخت\u200cخانوادگی این شخص را ببینند.'),
        ),
    ]
