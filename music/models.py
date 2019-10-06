from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=2048, db_index=True)
    artist = models.CharField(max_length=2048, blank=True, db_index=True)
    source = models.CharField(max_length=4096, blank=True)
    image = models.CharField(max_length=2048, blank=True)

    class Meta:
        ordering = ("id",)
        db_table = "songs"
