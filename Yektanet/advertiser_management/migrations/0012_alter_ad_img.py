# Generated by Django 4.0.1 on 2022-02-02 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0011_alter_ad_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='img',
            field=models.ImageField(upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
