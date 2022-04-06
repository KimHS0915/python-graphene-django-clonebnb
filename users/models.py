from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Custom User Model Definition """

    avatar = models.ImageField('avatar', upload_to='avatars', blank=True)
    birthdate = models.DateField('birthdate', blank=True, null=True)
    superhost = models.BooleanField('superhost', default=False)
    favs = models.ManyToManyField("rooms.Room", related_name="favs")

    def room_count(self):
        return self.rooms.count()

    room_count.short_description = "Room Count"
