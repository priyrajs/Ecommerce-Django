# Generated by Django 3.2.5 on 2021-07-26 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210726_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='firstname',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='lastname',
        ),
    ]
