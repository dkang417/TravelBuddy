from __future__ import unicode_literals

from django.db import models
from django.contrib import messages

import bcrypt
import datetime 

class UserManager(models.Manager):
    def validate(self, request):
        if request.method == "POST":
            valid = True
            for key in request.POST:
                if request.POST[key] == "":
                    valid = False
                    messages.error(request, "{} is required".format(key))
            if len(request.POST["password"]) <= 8:
            	valid= False 
            	messages.error(request, "password must be more than 8 characters")
            if len(request.POST["name"]) <=3:
            	valid = False
            	messages.error(request, "name must be more than 3 characters")
            if len(request.POST["username"]) <=3:
            	valid = False
            	messages.error(request, "username must be more than 3 characters")	
            if request.POST["password"] != request.POST["confirm_password"]:
                valid = False
                messages.error(request, "password must match confirm password")
            if valid:
            	name = request.POST["name"]
            	username = request.POST["username"]
            	password = request.POST["password"]
            	hashed_pw = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

                self.create(name=name, username=username, password=hashed_pw)
                messages.success(request, "Successfully registered!")

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
    	return "<User object: {} {}>".format(self.name,self.username)

    objects = UserManager()


class TripManager(models.Manager): 
    def validateTrip(self, request):

        if request.method == "POST":
            valid = True
            for key in request.POST:
                if request.POST[key] == "":
                    valid = False
                    messages.error(request, "{} is required".format(key))
            
            # check the dates 
            if request.POST['travel_date_from'] < str(datetime.datetime.today()):
                valid = False
                messages.error(request,"must be a future date")
            if request.POST['travel_date_to'] < request.POST['travel_date_from']:
                valid = False
                messages.error(request, "travel date to must not be before travel date from")

            if valid:
            #create the trip     
                user = User.objects.get(id=request.session['active_id'])
                destination = request.POST['destination']
                description = request.POST['description']
                travel_date_from = request.POST['travel_date_from']
                travel_date_to = request.POST['travel_date_to']
                self.create(destination = destination, description=description, travel_date_to = travel_date_to, travel_date_from = travel_date_from, creator=user)
                messages.success(request, "Successfully registered!")

                


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="createdtrips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, related_name="tripsjoined")
    objects = TripManager()
   

