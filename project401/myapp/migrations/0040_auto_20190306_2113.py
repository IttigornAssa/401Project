# Generated by Django 2.0.6 on 2019-03-06 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_auto_20190306_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardrecord',
            name='timestamp',
        ),
        migrations.DeleteModel(
            name='cardRecord',
        ),
        migrations.DeleteModel(
            name='timeStamp',
        ),
    ]