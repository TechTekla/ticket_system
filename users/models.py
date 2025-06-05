from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.models import AbstractUser


#what the database is supposed to have 
# firstame,second_name, phone number , email , gender, id,created ,updated 

class User(AbstractUser):
    gender =  [("male","male"),("female","female")]
    username  = models.CharField(unique =True,max_length =100)
    first_name  = models.CharField(max_length = 50,blank =  True)
    last_name = models.CharField(max_length = 50,blank = True )
    phone_number = models.CharField(max_length=10,default = 0000000000)
    email = models.EmailField(max_length = 100,unique = True,default = "ticket@gmail.com")
    gender =  models.CharField(choices = gender )
    id_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save (self ,*args, **kwargs):
        email_username,_ = self.email.split('@')
        if self.username == "" or self.username == None:
            self.username = email_username

        super(User,self).save(*args,**Kwargs)


    class Meta:
        ordering = ['-created_at']
