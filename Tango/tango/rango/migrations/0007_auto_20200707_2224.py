# Generated by Django 3.0.7 on 2020-07-07 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_rating_rating_average'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rating_average',
        ),
        migrations.AddField(
            model_name='rating',
            name='is_favorite',
            field=models.IntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=1),
        ),
    ]
