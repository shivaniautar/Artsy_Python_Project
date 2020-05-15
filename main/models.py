from django.db import models
from datetime import datetime, timedelta
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        if len(postData['usertype']) == 0:
            errors['usertype'] = "You must select a user type."
        # if len(postData['aboutyou']) == 0:
        #     errors['aboutyou'] = "You must tell us something about you."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "That email is already registered."
        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters."
        elif postData['password'] != postData['pw_confirm']:
            errors['password'] = "Password does not match confirmation."
        return errors

class ItemManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title'])<1:
            errors['title'] = "Title must be provided!"
        if len(postData['description'])<1:
            errors['description'] = "Description must be provided!"
        if len(postData['price'])<0:
            errors['price'] = "Price must be provided."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    usertype = models.CharField(max_length=64)
    aboutyou = models.TextField(max_length=300, blank=True )
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length = 60)
    image = models.ImageField(upload_to='profile_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Item(models.Model):
    image = models.ImageField(upload_to='item_pic')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='jobs')
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()

    def __str__(self):
        return str(self.title) + ": $" + str(self.price)