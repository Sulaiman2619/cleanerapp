
from typing import Any
from django.contrib.auth.models import User
from django.db import models
class Cleaner(models.Model):
    # Define choices for sex
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)

    def __str__(self):
        return self.user.first_name


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_floors = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    room_name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor_num = models.PositiveIntegerField()

    def __str__(self):
        return f" {self.building.name} ห้อง {self.room_name} ชั้น {self.floor_num}"

    class Meta:
        unique_together = ('room_name', 'building', 'floor_num')

class Work(models.Model):
    work_name = models.CharField(max_length=100)
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    WEEKDAYS = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
   # Use CharField with choices argument
    day = models.CharField(max_length=9, choices=WEEKDAYS)  # Set max_length to accommodate the longest weekday name
    def __str__(self):
        return f"Please {self.cleaner.user.first_name} {self.work_name} in {self.room} on {self.day}"

    class Meta:
        unique_together = ('work_name', 'cleaner', 'room', 'day')

class Checker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class WorksData(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=20)
    rating = models.IntegerField(default=0)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    staff = models.CharField(max_length=100)
    
    def __str__(self):
        return f"WorksData for Work {self.work_id}, Status: {self.status}"
    

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
       return self.user.first_name

