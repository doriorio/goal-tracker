# Generated by Django 2.2.7 on 2019-12-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20191224_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='mood',
            field=models.CharField(choices=[('H', '😄'), ('M', '😐'), ('S', '😔 ')], default='M', max_length=1),
        ),
    ]
