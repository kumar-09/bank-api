# Generated by Django 5.0.3 on 2024-03-07 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_accountno'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='account_images/'),
        ),
    ]
