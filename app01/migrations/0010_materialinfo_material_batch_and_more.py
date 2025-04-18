# Generated by Django 4.2 on 2023-04-18 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_rename_foodmaterialinfo_materialinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialinfo',
            name='material_batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='material_batch', to='app01.foodbatchinfo', verbose_name='产品批次'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='materialinfo',
            name='product_batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_batch', to='app01.foodbatchinfo', verbose_name='产品批次'),
            preserve_default=False,
        ),
    ]
