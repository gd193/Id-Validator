# Generated by Django 2.2.2 on 2019-08-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0002_delete_id_generator'),
    ]

    operations = [
        migrations.AddField(
            model_name='id',
            name='Validated',
            field=models.BooleanField(default=False),
        ),
    ]
