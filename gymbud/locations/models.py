# from django.db import models
# import uuid
# from django.utils import timezone

# class Places(models.Model):
#     id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     city        = models.CharField(max_length=20)
#     street      = models.CharField(max_length=20)
#     state       = models.CharField(max_length=20)
#     country     = models.CharField(max_length=20)
#     placeId     = models.CharField(max_length=100)
#     latitude    = models.FloatField(blank=True, null=True)
#     longitude   = models.FloatField(blank=True, null=True)
#     dateCreated = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(f"{self.city} {self.street}")


# class Gym(models.Model):
#     id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name        = models.CharField(max_length=20)
#     place       = models.ForeignKey(Places, on_delete=models.CASCADE)
#     date        = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(f"{self.name}")

# class Exercise(models.Model):

#     id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name        = models.CharField(max_length=40)
#     category    = models.CharField(max_length=20)
#     authorized  = models.BooleanField(default=False)
#     dateCreated = models.DateTimeField(auto_now_add=True)
    


# class FavoriteExercises(models.Model):
#     id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user        = models.ForeignKey(User, on_delete=models.CASCADE)
#     exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
#     date        = models.DateTimeField(auto_now_add=True)
    

#     def __str__(self):
#         return str(f"{self.user} favorited {self.exercise} on {self.date}")
    
# class SocialLinks(models.Model):
    
#     SocialLinksType = [
#         ("1", "Facebook"),
#         ("2", "Instagram"),
#         ("3", "Twitter")
#     ]

#     id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user        = models.ForeignKey(User, on_delete=models.CASCADE)
#     type        = models.CharField(max_length=12, null=True, choices=SocialLinksType)
#     link        = models.CharField(max_length=100)
#     date        = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(f"{self.user} favorited {self.link}")