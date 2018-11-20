from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages, sessions
from . models import *
from datetime import datetime
import bcrypt

def index(request):

    return render(request, 'login_registration_app/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['email'] = request.POST['email']
    request.session['birthdate'] = request.POST['birthdate']
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode('utf8'), bcrypt.gensalt())
        newUser = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        birthdate=request.POST['birthdate'],
        password=hash1.decode('utf8'))
    return redirect('/wishes')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/')

    emailCheck = User.objects.filter(email=request.POST['email'])
    loginUser = emailCheck[0]
    newDate = datetime.strftime(loginUser.birthdate, "%Y-%m-%d")

    if bcrypt.checkpw(request.POST['password'].encode('utf8'), loginUser.password.encode('utf8')):
        request.session['userId'] = loginUser.id
        request.session['firstName'] = loginUser.first_name
    if newDate == request.POST['birthdate']:
        return redirect('/wishes')
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')





def wishes(request):
    if "userId" not in request.session:
        return redirect('/')

    wishes = Wish.objects.all().order_by('-created_at')
    show = {
        'wishes': wishes,
    }


    return render(request, 'login_registration_app/wishes.html', show)




def newWish(request):
    if "userId" not in request.session:
        return redirect("/")


    return render(request, 'login_registration_app/newWish.html')

def wishHandler(request):
    if "userId" not in request.session:
        return redirect("/")
    else:
        errors = Wish.objects.wishValidator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
                return redirect('/wishes/new/')
            
        addWish = Wish.objects.create(
        wish = request.POST['wish'],
        description = request.POST['description'],
        poster = User.objects.get(id=request.session['userId']),
        )
    
    return redirect('/wishes')
    





def editWish(request, id):
    print('YOU ARE HERE', id)
    wish = Wish.objects.get(id=id)
    wishes = {
        "id": id,
        "wish": wish
    }
    return render(request, 'login_registration_app/editWish.html', wishes)


def grantWish(request, id):
    grantWish = Wish.objects.get(id=id)
    grantWish.is_GrantedWish = 1
    grantWish.save()
    return redirect('/wishes')


def editor(request):

    print("I GOT HERE")
    wish_edit = Wish.objects.get(id=request.POST['id'])
    wish_edit.wish = request.POST['wish']
    wish_edit.description = request.POST['description']
    wish_edit.save()

    return redirect('/wishes')


def like(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id=request.session["userId"])
    wish.usersWishes.add(user)
    wish.save()



    return redirect("/wishes")


def remove(request, id):
    remove = Wish.objects.get(id=id)
    remove.delete()
    return redirect('/wishes')





def stats(request):
    return render(request, 'login_registration_app/stats.html')

