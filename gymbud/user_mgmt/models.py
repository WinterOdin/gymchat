import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from locations.models import Places, Gym


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email       = models.EmailField(_('email address'), unique=True)
    first_name  = models.CharField(max_length=150, blank=True)
    start_date  = models.DateTimeField(default=timezone.now)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

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
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    swiped_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date        = models.DateTimeField(auto_now_add=True)
    swipe       = models.CharField(max_length=20, default="like", choices=(SwipeChoices))

    def __str__(self):
        return str(f"{self.user} swiped {self.swiped_user} on {self.date}")
    
class Matches(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    matched_user= models.ForeignKey(User, on_delete=models.CASCADE)
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} matched with {self.matched_user} on {self.date}")
    
class NotMatches(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    not_matched_user= models.ForeignKey(User, on_delete=models.CASCADE)
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} not matched with {self.not_matched_user} on {self.date}")
    
class FavoriteExercises(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise    = models.CharField(max_length=12)
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
    type        = models.CharField(max_length=12, null=True, choices=SocialLinksType)
    link        = models.CharField(max_length=100)
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} favorited {self.exercise} on {self.date}")

#for now we are extening base user model in next step we need to connect with 
#auth 
class Profile(models.Model):

    GENDER = [
        ("1", "Male"),
        ("2", "Female"),
        ("3", "Other")
    ]

    EXERCISES = [
        ("1", "Lateral Raiise"),
        ("2", "Bench Press"),
        ("3", "Squats")
    ]

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    gym             = models.ForeignKey(Gym, on_delete=models.CASCADE)
    gender          = models.CharField(max_length=10, null=True, choices=GENDER)
    bio             = models.TextField(null=True)
    place           = models.ForeignKey(Places, on_delete=models.CASCADE)
    playlist        = models.CharField(max_length=25, null=True)
    dateCreated     = models.DateTimeField(auto_now_add=True)
    dateUpdated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.email)

    @property
    def num_likes(self):
        return self.matched.all().count()
    






#for tinder matching
# class MachedRoom(models.Model):
#     id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     protagonist         = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("main_person"),
#                                related_name='top_person')
#     contestant_left     = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("left"),
#                                related_name='left_person')
#     contestant_right    = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("right"),
#                                related_name='right_person')

#     max_votes           = models.PositiveIntegerField()
#     votes_left          = models.PositiveIntegerField()
#     votes_right         = models.PositiveIntegerField()
#     dateCreated         = models.DateTimeField(auto_now_add=True)


    
#     @staticmethod
#     def return_winner(self):
#         if self.votes_left > votes_right:
#             return Profile.objects.get(profile_id=self.contestant_left)
#         else:
#             return Profile.objects.get(profile_id=self.contestant_right)

#     #return %
