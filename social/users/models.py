from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .choices import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True,on_delete=models.CASCADE)

    @classmethod
    def addfriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def removefriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

        def __str__(self):
            return f'{self.current_user.username} Friends'


class Interest(models.Model):
    movie = models.CharField(choices=MovieChoices, max_length=50, null=True, blank=True, default=MovieChoices[4][1])
    music = models.CharField(choices=MusicChoices, max_length=50, null=True, blank=True, default=MusicChoices[4][1])
    food = models.CharField(choices=FoodChoices, max_length=50, null=True, blank=True, default=FoodChoices[4][1])
    sports = models.CharField(choices=SportsChoices, max_length=50, null=True, blank=True, default=SportsChoices[4][1])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Interests'