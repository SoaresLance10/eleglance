# Generated by Django 3.1.4 on 2021-07-14 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20210714_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistitem',
            name='date_added',
            field=models.DateField(blank=True, null=True),
        ),
    ]
