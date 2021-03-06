# Generated by Django 4.0.1 on 2022-02-17 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0027_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clicks_count', models.PositiveIntegerField(verbose_name='Clicks Count')),
                ('views_count', models.PositiveIntegerField(verbose_name='Clicks Count')),
                ('ad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hourly_stats', to='advertiser_management.ad')),
            ],
        ),
        migrations.DeleteModel(
            name='Stats',
        ),
    ]
