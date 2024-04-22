from django.db import models
from django.conf import settings

# Create your models here.

class Room(models.Model):
    room_categories = (
        ('YAC', 'AC Room'),
        ('NAC', 'Non AC Room'),
        ('DEL', 'Deluxe Suite'),
        ('KIN','King Suite'),
        ('QUE', 'Queen Suite'),
        ('NAU', 'Naukar Room'),
    )
    room_number = models.IntegerField()
    categories = models.CharField(max_length = 3, choices = room_categories)
    no_of_beds = models.IntegerField()
    room_capacity = models.IntegerField()
    def __str__(self):
        return f'{self.room_number}. {self.categories} with {self.no_of_beds} beds for {self.room_capacity} people'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE) 
    Check_In_Time = models.DateTimeField()
    Check_Out_Time = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.Check_In_Time} to {self.Check_Out_Time}'