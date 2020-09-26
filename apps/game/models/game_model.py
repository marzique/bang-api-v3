from django.db import models


class Game(models.Model):
    started = models.BooleanField(default=False)

    def __str__(self):
        return f'Game #{self.pk}'