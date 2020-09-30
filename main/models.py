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

class Address(models.Model):
    address = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


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
    address = models.ForeignKey(Address, related_name="user",null=True, on_delete=models.CASCADE)

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

class Cart(models.Model):
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class CreditCard(models.Model):
    number = models.IntegerField()
    security_code = models.IntegerField()
    expiration_date = models.DateField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    address = models.ForeignKey(Address, related_name="card", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="credit_cards", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    status = models.CharField(max_length=45)
    cart = models.OneToOneField(Cart,on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    credit_card = models.ForeignKey(CreditCard, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.title) + ": $" + str(self.price)