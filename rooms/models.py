from django.db import models


class Rooms(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)
    more = models.TextField()

    def __str__(self):
        return str(self.name) + ' ' + str(self.capacity)


class Reservation(models.Model):
    reservation_date = models.DateField()
    room_id = models.ManyToManyField(Rooms)
    comment = models.TextField()

    def __str__(self):
        return str(self.reservation_date) + ' ' + str(self.comment)