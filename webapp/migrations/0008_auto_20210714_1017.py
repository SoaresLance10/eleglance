# Generated by Django 3.1.4 on 2021-07-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20210714_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='date_submitted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='diamond_quality',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='gold_purity',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='gold_weight',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]