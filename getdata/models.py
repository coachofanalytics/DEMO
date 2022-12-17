from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Driver_Details(models.Model):
	id = models.AutoField(primary_key=True)
	driver_name = models.CharField(max_length=1000,null=True,blank=True)

class Location_Data(models.Model):
	id = models.AutoField(primary_key=True)
	country = models.CharField(max_length=500,null=True,blank=True)
	state = models.CharField(max_length=500,null=True,blank=True)
	city = models.CharField(max_length=500,null=True,blank=True)
	location_name = models.CharField(max_length=1000,null=True,blank=True)

class Daily_Date(models.Model):
	id = models.AutoField(primary_key=True)
	dates = models.DateTimeField(auto_now_add=True)

class Meteorological_Data(models.Model):
	id = models.AutoField(primary_key=True)
	driver =  models.ForeignKey(Driver_Details, on_delete=models.CASCADE, related_name='Driver_Details_1')
	location =  models.ForeignKey(Location_Data, on_delete=models.CASCADE)
	meteorological_date = models.ForeignKey(Daily_Date, on_delete=models.CASCADE)
	meteorological_time = models.CharField(max_length=100,null=True,blank=True)
	temperature = models.FloatField(null=True, blank=True) #celsius value
	wind_speed = models.FloatField(null=True, blank=True)  #km/h value
	rainfall = models.FloatField(null=True, blank=True)   # mile meter value
	humidity = models.FloatField(null=True, blank=True)
	pressure = models.FloatField(null=True, blank=True)


class NTSA_Crash_Data(models.Model):
	id = models.AutoField(primary_key=True)
	driver =  models.ForeignKey(Driver_Details, on_delete=models.CASCADE, related_name='Driver_Details_2')
	crash_location = models.ForeignKey(Location_Data, on_delete=models.CASCADE)
	crash_date = models.ForeignKey(Daily_Date, on_delete=models.CASCADE)
	crash_time = models.CharField(max_length=100,null=True,blank=True)
	crash_severity = models.CharField(max_length=500,null=True, blank=True) #(high,medium,low)
	crash_type = models.CharField(max_length=500,null=True, blank=True) #(Fatal,Injury,Property Damage Only)
	crash_vehicle_count = models.CharField(max_length=500,null=True, blank=True)
	vechicle_name = models.CharField(max_length=500,null=True, blank=True)
	vechicle_type = models.CharField(max_length=500,null=True, blank=True)
	crash_reason = models.CharField(max_length=500,null=True, blank=True) #(weather,alcohal,distracted_driving,animal,Traffic crash)
	weather_type = models.CharField(max_length=500,null=True, blank=True)


class Traffic_Data(models.Model):
	id = models.AutoField(primary_key=True)
	driver =  models.ForeignKey(Driver_Details, on_delete=models.CASCADE,related_name='Driver_Details_3')
	location = models.ForeignKey(Location_Data, on_delete=models.CASCADE)
	traffic_date = models.ForeignKey(Daily_Date, on_delete=models.CASCADE)
	total_vechicle = models.IntegerField(null=True,blank=True)
	speed_limit = models.FloatField(null=True, blank=True)
	max_speed = models.FloatField(null=True, blank=True)
	min_speed = models.FloatField(null=True, blank=True)
	average_speed = models.FloatField(null=True, blank=True)
	traffic_occur_perday_count = models.IntegerField(null=True, blank=True)
	traffic_reason = models.CharField(max_length=500,null=True, blank=True)
	traffic_level = models.CharField(max_length=500,null=True, blank=True)
	road_category = models.CharField(max_length=500,null=True, blank=True)



class Air_Quality_Data(models.Model):
	id = models.AutoField(primary_key=True)
	driver =  models.ForeignKey(Driver_Details, on_delete=models.CASCADE, related_name='Driver_Details_4')
	location =  models.ForeignKey(Location_Data, on_delete=models.CASCADE)
	air_quality_date = models.ForeignKey(Daily_Date, on_delete=models.CASCADE)
	air_quality_time = models.CharField(max_length=100,null=True,blank=True)
	particulate_matter = models.FloatField(null=True, blank=True) # µm 
	air_quality_index = models.IntegerField(null=True, blank=True) #(0-50--good,51-100--satisfactory,101-200--moderate,201-300 --poor,301-400 --very poor,401-500 --severe)


class CashappMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	full_path = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)
	parsed_date = models.DateTimeField(auto_now_add=True)


class ReplyMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)


class stockmarket(models.Model):
	symbol = models.CharField(max_length=255)
	action = models.CharField(max_length=255)
	qty=models.PositiveIntegerField()
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField()

class cryptomarket(models.Model):
	symbol = models.CharField(max_length=255)
	action = models.CharField(max_length=255)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField()

	def __str__(self):
		return self.symbol
