# Generated by Django 4.2.1 on 2024-05-09 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_auto_20240510_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='fadax_payment',
            name='transactionId',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='شماره تراکنش'),
        ),
        migrations.AlterField(
            model_name='fadax_payment',
            name='fadaxTrackingNumber',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='کد رهگیری فدکس'),
        ),
    ]
