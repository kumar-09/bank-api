# Generated by Django 5.0.3 on 2024-03-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_account_mobile_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='amount',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
