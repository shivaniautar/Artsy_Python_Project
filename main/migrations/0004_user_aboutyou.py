# Generated by Django 2.2 on 2020-04-28 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200428_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aboutyou',
            field=models.TextField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
