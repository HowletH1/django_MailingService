# Generated by Django 4.2.5 on 2023-09-13 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_mailing_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglogs',
            name='mailing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.mailing'),
            preserve_default=False,
        ),
    ]
