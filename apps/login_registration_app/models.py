from __future__ import unicode_literals
from django.db import models
import re
import datetime
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
WORD_SPACE_REGEX = re.compile(r'^[A-Za-z ]+')



class validator(models.Manager):
    def basic_validator(self, postData):
        now = datetime.datetime.now()
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = '*Required; No fewer than 2 characters; letters only'
        if not WORD_SPACE_REGEX.match(postData['first_name']):
            errors['first_name'] = '*Required; No fewer than 2 characters; letters only'
        if len(postData['last_name']) < 2:
            errors['last_name'] = '*Required; No fewer than 2 characters; letters only'
        if not WORD_SPACE_REGEX.match(postData['last_name']):
            errors['last_name'] = '*Required; No fewer than 2 characters; letters only'
        if len(postData['email']) == 0:
            errors['email'] = '*Required; No fewer than 2 characters; valid email@format.please'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = '*Required; No fewer than 2 characters; valid email@format.please'
        email_check = User.objects.filter(email=postData['email'])
        if len(email_check) > 0:
            errors['taken'] = '*Email already taken!'
        if len(postData['password']) == 0:
            errors['password'] = '*Required; Password must be minimum 8 characters'
        if not re.search('[0-9]', postData['password']):
            errors['password'] = '*Required; Password must contain numbers'
        if not re.search('[A-Z]', postData['password']):
            errors['password'] = '*Required; Password must contain one Capital letter'
        if postData['password'] != postData['confirm']:
            errors['confirm'] = '*Password must match!!!'
        if str(postData['birthdate']) == str(now.strftime("%Y-%m-%d")):
            errors['birthdate'] = '*Birthdate prior todays date is required'
        return errors

    def login_validator(self, postData):
        errors ={}
        if len(postData['email']) == 0:
            errors['login'] = '*Something went wrong.'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['login'] = '*Something went wrong.'
        if len(postData['birthdate']) == 0:
            errors['login_birthdate'] = '*Something went wrong.'
        return errors


class anotherValidator(models.Manager):
    def wishValidator(self, postData):
        errors = {}
        if(len(postData["wish"]) == 0):
            errors["wish"] = "Wish field cannot be left blank"
        if(len(postData["wish"]) <= 3):
            errors["wish"] = "A wish must consist of at least 3 characters!"
        if(len(postData["description"]) == 0):
            errors["description"] = "Description field cannot be left blank"
        if(len(postData["description"]) <= 3):
            errors["plan"] = "A description must consist of at least 3 characters"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    confirm = models.CharField(max_length=250)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = validator()


class Wish(models.Model):
    wish = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="wisher", null=True)
    usersWishes = models.ManyToManyField(User, related_name="grantsWishes")
    is_GrantedWish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = anotherValidator()
