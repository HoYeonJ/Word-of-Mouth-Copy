from django.db import models
from django import forms 
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from multiselectfield import MultiSelectField
import csv
import datetime
# Create your models here.
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

ingredients_list = []

class FoodList(models.Model):
	title = models.CharField(max_length=500, choices = tuple(ingredients_list))

class RecipePost(models.Model):
	user = models.ForeignKey(User, default = 1, null = True, on_delete = models.SET_NULL)
	title = models.CharField(max_length=200, default='Recipe Title')
	author = models.CharField(max_length=200, default='Author')
	ingredients = models.TextField(default='Ingredients')
	intro = models.TextField(default='Instructions')
	cook_time = models.IntegerField(default=0)
	servings = models.IntegerField(default=0)
	pub_date = models.DateTimeField(default=now)
	saved = models.ManyToManyField(User, related_name='saved', default=None, blank=True)
	recipe_image = models.ImageField(upload_to='images/', default='images/wordofmouth.png')
	forked = models.IntegerField(default=0)
	forkedid = models.IntegerField(default=0) 
	def __str__(self):
		return self.title
	def cook_time_valid(self):
		return 0 <= self.cook_time
	def servings_valid(self):
		return 0 <= self.servings
	def forked_recipes(self):
		return RecipePost.objects.get_queryset().filter(isForked = 1, forkedid = self.id)

class RecipeForm(forms.ModelForm):
	def __str__(self):
		return self.title
	class Meta:
		model = RecipePost
		fields = ['title', 'author', 'intro', 'ingredients', 'cook_time', 'servings', 'recipe_image']
		#'__all__'
		ingredients = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=ingredients_list)


