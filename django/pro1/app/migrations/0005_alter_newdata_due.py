# Generated by Django 4.2.5 on 2023-09-26 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_newdata_is_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newdata',
            name='due',
            field=models.DateField(default='No due date'),
        ),
    ]
