# Generated by Django 3.1.5 on 2021-02-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notam',
            name='message',
            field=models.CharField(max_length=511),
        ),
    ]
