# Generated by Django 4.2 on 2023-04-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_flowrecord_enterpriseid_flowrecord_userid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodinfo',
            name='name',
            field=models.CharField(max_length=50, verbose_name='食品名称'),
        ),
    ]
