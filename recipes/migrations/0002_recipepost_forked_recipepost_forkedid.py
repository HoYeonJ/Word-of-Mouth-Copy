# Generated by Django 4.0.2 on 2022-05-03 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipepost',
            name='forked',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipepost',
            name='forkedid',
            field=models.IntegerField(default=0),
        ),
    ]
