# Generated by Django 2.2 on 2019-12-25 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191224_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='intro',
            field=models.CharField(default='', max_length=500),
        ),
    ]