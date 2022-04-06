from django.db import models
from common.models import AbstractTimeStampedModel

class Photo(AbstractTimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to='room_photos')
    room = models.ForeignKey(
        'Room', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(AbstractTimeStampedModel):
    """ Room Model Definitions """

    name = models.CharField(max_length=140)
    description = models.TextField()
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField(default="00:00:00")
    check_out = models.TimeField(default="00:00:00")
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name='rooms', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    def photo_number(self):
        return self.photos.count()
    
    photo_number.short_description = "Photo Count"

    class Meta:
        ordering = ('-created',)