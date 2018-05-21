from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if "active_id" in request.session:
        return redirect('/travels')
    return render(request, "travel/index.html")

def register(request):
    User.objects.validate(request)
    return redirect("/main")

def login(request):
    users = User.objects.filter(username=request.POST["username"])
    if len(users) > 0:
        user = users[0]
        password = request.POST['password']
        newPassword = bcrypt.checkpw(password.encode(), user.password.encode())
        if newPassword: 
            request.session["active_id"] = user.id 
            return redirect('/travels')
         
    messages.error(request, "Invalid login information")
    return redirect("/")

def travels(request):
	if request.session.get('active_id') == None:
		return redirect('/')
	
	user_trips= Trip.objects.filter(creator_id=User.objects.get(id=request.session['active_id']))
	user = User.objects.get(id=request.session['active_id'])

	#exclude trips user created and joined
	other_trips = Trip.objects.exclude(creator__id=request.session['active_id']).exclude(members__id=request.session['active_id'])

	# get the trips user joined 
	joined_trips =user.tripsjoined.all()

	context = {
		'user' : user,
		'user_trips':user_trips,
		'other_trips': other_trips,
		'joined_trips': joined_trips
	}
	return render(request, 'travel/travels.html', context)

def add(request):
	if request.session.get('active_id') == None:
		return redirect('/')
	return render(request, 'travel/add.html')

def addtrip(request):   
	
	Trip.objects.validateTrip(request)
	return redirect("/travels")


def join(request,id):
	user = User.objects.get(id=request.session['active_id'])
	trip= Trip.objects.get(id=id)
	
	trip.members.add(user)
	
	return redirect("/travels")

def showtrip(request,id):
	user = User.objects.get(id=request.session['active_id'])
	trip = Trip.objects.get(id=id)

	members= trip.members.all()

	context = {
		'user': user,
		'trip': trip,
		'members': members 
	}

	return render( request, 'travel/showtrip.html', context)


def logout(request):
	request.session.clear()
	return redirect('/')