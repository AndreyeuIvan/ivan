from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True, blank=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)


	def __str__(self):
		return self.name


class Page(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	
	
	def __str__(self):
		return self.title


class Rating(models.Model):
	'''Here I want to rate my Pages'''
	Rating_CHOICES = (
    (1, 'Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent')
)

	is_favorite = models.IntegerField(choices=Rating_CHOICES, default=1)
	review = models.CharField(max_length=128)
	page = models.ForeignKey(Page, on_delete=models.CASCADE)



	def __str__(self):
		return self.review


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to = 'profile_images', blank=True)


	def __str__(self):
		return self.user.username