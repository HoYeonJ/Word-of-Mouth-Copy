# test cases, client, asserts:
# https://docs.djangoproject.com/en/4.0/topics/testing/tools/
# reverse:
# https://docs.djangoproject.com/en/4.0/ref/urlresolvers/
# login testing:
# https://adamj.eu/tech/2020/06/15/how-to-unit-test-a-django-form/
from django.test import TestCase
from django.test import Client
from recipes.models import RecipePost
from django.utils import timezone
from django.utils.timezone import now
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from http import HTTPStatus


class RecipePostTestCase(TestCase):

	def test_recipe_title(self):
		recipe = RecipePost(title="Apple Pie")
		self.assertEqual(str(recipe), 'Apple Pie')

	def test_recipe_author(self):
		recipe = RecipePost(title="Apple Pie", author="joe")
		self.assertEqual(str(recipe.author), 'joe')

	def test_recipe_intro(self):
		recipe = RecipePost(intro="intro for recipe")
		self.assertEqual(str(recipe.intro), 'intro for recipe')

	def test_recipe_cooktime(self):
		recipe = RecipePost(cook_time=45)
		self.assertEqual(str(recipe.cook_time), '45')

	def test_recipe_servings(self):
		recipe = RecipePost(servings=25)
		self.assertEqual(str(recipe.servings), '25')

class RecipeValidEntry(TestCase):

	def test_valid_cooktime(self):
		recipe = RecipePost(cook_time=-10)
		self.assertIs(recipe.cook_time_valid(), False)

	def test_valid_servings(self):
		recipe = RecipePost(servings=-20)
		self.assertIs(recipe.servings_valid(), False)

class AccountCredentials(TestCase):

	def test_login(self):
		self.user = User.objects.create_user(username="testuser")
		self.user.set_password("123456Ab")
		self.user.save()
		c = Client()
		self.assertEqual(c.login(username="testuser", password="123456Ab"),True)

	def test_signup(self):
		response=self.client.post("/accounts/signup/", {'id_username': 'testuser1', 'id_email': 'testuser@email.com', 'id_password1': '123456Ab', "id_password2": "123456Ab"})
		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_signup_wrong_password(self):
		response=self.client.post("/accounts/signup/", {'id_username': 'testuser1', 'id_email': 'testuser@email.com', 'id_password1': '123456Ac', "id_password2": "123456Ab"})
		self.assertEqual(response.status_code, HTTPStatus.OK)

class DeleteAndEditRecipes(TestCase):

	# def test_no_recipes(self):
	# 	"""
	# 	No recipes are shown in feed if none are created.
	# 	"""
	# 	response = self.client.get(reverse('recipes:feed'))
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertContains(response, "No recipes are available.")
	# 	self.assertQuerysetEqual(response.context['recipes_list'], [])

	def test_one_recipes(self):
		"""
		No recipes are shown in feed if none are created.
		"""
		self.user = User.objects.create_user(username='testuser', password='12345')
		login = self.client.login(username='testuser', password='12345')
		recipe = RecipePost.objects.create(title="Cheeseburger")
		response = self.client.get(reverse('recipes:feed'))
		self.assertQuerysetEqual(response.context['recipes_list'], [recipe],)

