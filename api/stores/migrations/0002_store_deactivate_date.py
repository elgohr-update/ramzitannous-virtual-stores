# Generated by Django 3.0.6 on 2020-05-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='deactivate_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
