# Generated by Django 3.1.1 on 2020-09-27 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20200926_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='game.game'),
        ),
    ]
