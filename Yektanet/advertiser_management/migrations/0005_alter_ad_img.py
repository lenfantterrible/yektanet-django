# Generated by Django 4.0.1 on 2022-02-01 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0004_alter_ad_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='img',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]
