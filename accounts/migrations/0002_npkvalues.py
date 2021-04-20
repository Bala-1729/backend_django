# Generated by Django 3.2 on 2021-04-20 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPKValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.FloatField(null=True)),
                ('p', models.FloatField(null=True)),
                ('k', models.FloatField(null=True)),
                ('deviceId', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]
