from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.



class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)

    def __str__(self):
        return str(f"{self.name} {self.city}")

#for now we are extening base user model in next step we need to connect with 
#auth 
class Profile(models.Model):

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ]

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    gym             = models.ForeignKey(Gym, on_delete=models.CASCADE)
    matched         = models.ManyToManyField(User, related_name="likes", blank=True)
    blocked_by      = models.ManyToManyField(User, related_name="blocked", blank=True)
    fav_exercise    = models.CharField(max_length=12, null=True)
    gender          = models.CharField(max_length=10, null=True, choices=GENDER)
    bio             = models.TextField(null=True)
    city            = models.CharField(max_length=25, null=True)
    country         = models.CharField(max_length=25, null=True)
    swipes_left     = models.PositiveIntegerField(null=True)
    swipes_right    = models.PositiveIntegerField(null=True)
    playlist        = models.CharField(max_length=25, null=True)
    instagram       = models.CharField(max_length=25, null=True)
    dateCreated     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    @property
    def num_likes(self):
        return self.matched.all().count()
    

