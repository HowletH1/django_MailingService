# Generated by Django 4.2.5 on 2023-09-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_mailinglogs_mailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Статус клиента'),
        ),
    ]