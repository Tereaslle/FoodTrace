# Generated by Django 4.2 on 2023-04-24 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_materialinfo_material_batch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodinfo',
            name='permission_code',
        ),
        migrations.AddField(
            model_name='enterpriseinfo',
            name='permission_code',
            field=models.CharField(default=123, max_length=16, verbose_name='食品生产许可证编号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodbatchinfo',
            name='amount',
            field=models.CharField(default='0', max_length=20, verbose_name='数量'),
        ),
        migrations.AddField(
            model_name='foodbatchinfo',
            name='quality',
            field=models.TextField(default='无', verbose_name='验收信息'),
        ),
        migrations.AddField(
            model_name='singlefoodinfo',
            name='weight',
            field=models.CharField(default='0', max_length=20, verbose_name='质量'),
        ),
        migrations.AlterField(
            model_name='materialinfo',
            name='material_batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_batch', to='app01.foodbatchinfo', verbose_name='原材料批次'),
        ),
    ]
