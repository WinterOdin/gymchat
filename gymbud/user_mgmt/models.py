import uuid
from datetime import date
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

 
class Location(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city        = models.CharField(max_length=20)
    street      = models.CharField(max_length=20)
    state       = models.CharField(max_length=20)
    country     = models.CharField(max_length=20)
    placeId     = models.CharField(max_length=100)
    latitude    = models.FloatField(blank=True, null=True)
    longitude   = models.FloatField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.city} {self.street}")
        

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, birthday, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, birthday, **other_fields)

    def age_restriction(self, dob):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        return age

    def create_user(self, email, first_name, password, birthday, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        
        if not birthday:
            raise ValueError(_('You must provide a date of birth'))
        age = self.age_restriction(birthday)
        if age < 18:
            raise ValueError(_('You are to young'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email       = models.EmailField(_('email address'), unique=True)
    first_name  = models.CharField(max_length=150, blank=True)
    birthday    = models.DateField(blank=True, null=True)
    age         = models.PositiveIntegerField(blank=True, null=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="location", null=True)
    search_range = models.PositiveSmallIntegerField(default=10, blank=True, null=True)
    start_date  = models.DateTimeField(default=timezone.now)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)

    objects = CustomAccountManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'birthday']

    def __str__(self):
        return self.email


class UserPhoto(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    order   = models.PositiveIntegerField(null=True)
    url     = models.CharField(max_length=220)

    def __str__(self):
        return str(f"{self.url}")

class UserSwipe(models.Model):
    SwipeChoices = (
        ("like", "like"),
        ("dislike", "dislike"),
    )

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_user")
    swiped_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="swiped_user")
    date        = models.DateTimeField(auto_now_add=True)
    swipe       = models.CharField(max_length=20, default="like", choices=(SwipeChoices))

    def __str__(self):
        return str(f"{self.user} swiped {self.swiped_user} on {self.date}")
    
class Matches(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_first_user")
    matched_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_second_user")
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} matched with {self.matched_user} on {self.date}")
    
class NotMatches(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notmatch_first_user")
    matched_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="notmatch_second_user")
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} not matched with {self.matched_user} on {self.date}")
    


class Gym(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=20)
    place       = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="gym_location")
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.name} {self.place.city} {self.place.street}")

class Exercise(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=40)
    category    = models.CharField(max_length=20)
    authorized  = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(f"{self.name}")


class FavoriteExercise(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date        = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(f"{self.user} favorited {self.exercise} on {self.date}")
    
class SocialLinks(models.Model):
    
    SocialLinksType = [
        ("1", "Facebook"),
        ("2", "Instagram"),
        ("3", "Twitter")
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    social_type = models.CharField(max_length=12, choices=SocialLinksType)
    link        = models.CharField(max_length=100)
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} favorited {self.link}")

class Profile(models.Model):

    GENDER = [
        ("1", "Male"),
        ("2", "Female"),
        ("3", "Other")
    ]


    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    gym             = models.OneToOneField(Gym, null=True, blank=True, on_delete=models.SET_NULL)
    gender          = models.CharField(max_length=10, choices=GENDER)
    bio             = models.TextField(null=True, blank=True)
    playlist        = models.CharField(max_length=25, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.email)

    @property
    def num_likes(self):
        return self.matched.all().count()

class Blocked(models.Model):
    
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_thats_blocking")
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_user")
    date_created = models.DateTimeField(auto_now_add=True)
