# Generated by Django 3.1.1 on 2020-09-25 16:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(blank=True, choices=[('SH', 'Sheriff'), ('RE', 'Renegade'), ('OL', 'Outlaw'), ('DE', 'Deputy')], max_length=2)),
                ('character', models.CharField(blank=True, choices=[('BC', 'Bart Cassidy'), ('BJ', 'Black Jack'), ('CJ', 'Calamity Janet'), ('EG', 'El Gringo'), ('JJ', 'Jesse Jones'), ('JD', 'Jourdonnais'), ('KC', 'Kit Carlson'), ('LD', 'Lucky Duke'), ('PL', 'Paul Regret'), ('PR', 'Pedro Ramirez'), ('RD', 'Rose Doolan'), ('SK', 'Sid Ketchum'), ('TK', 'Slab the Killer'), ('SL', 'Suzy Lafayette'), ('VS', 'Vulture Sam'), ('WK', 'Willy the Kid')], max_length=2)),
                ('health', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
