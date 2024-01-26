# Generated by Django 4.2.6 on 2023-11-30 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='groups',
        ),
        migrations.AddField(
            model_name='group',
            name='category',
            field=models.ManyToManyField(to='webapp.category'),
        ),
    ]