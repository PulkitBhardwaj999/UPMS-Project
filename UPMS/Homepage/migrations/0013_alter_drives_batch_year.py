# Generated by Django 5.0.1 on 2024-04-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0012_alter_drives_batch_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drives',
            name='batch_year',
            field=models.IntegerField(default=2024, verbose_name='year'),
        ),
    ]
