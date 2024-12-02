from django.db import models
# from .validators import validate_email, validate_phone_number, validate_location 

class LocationDetails(models.Model):
    location = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True,max_length=20)
    pin_code = models.CharField(max_length=6)
    state = models.CharField(max_length=100)
    number=models.IntegerField(unique=True,max_length=20)

    def __str__(self):
        return self.location

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    location=models.ForeignKey(LocationDetails,related_name='specialities',on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    doctor_name = models.CharField(max_length=100)
    speciality = models.ForeignKey(Speciality, related_name='doctors', on_delete=models.CASCADE)
    locations = models.ManyToManyField(LocationDetails, related_name='doctors')

    def __str__(self):
        return self.doctor_name