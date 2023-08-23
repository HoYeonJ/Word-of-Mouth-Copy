
# Cloud storage:
# https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
# https://cloud.google.com/python/django/appengine
# Searching: 
# https://stackoverflow.com/questions/11743207/django-model-case-insensitive-query-filtering
# Deleting a recipe post:
# https://stackoverflow.com/questions/19754103/django-how-to-delete-an-object-using-a-view
# Filtering a queryset:
# https://django-filter.readthedocs.io/en/stable/guide/usage.html
# https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class
# https://www.mytecbits.com/internet/python/addding-image-django-web-app
# https://www.w3schools.com/cssref/pr_background-image.asp
# https://webflow.com/blog/how-and-why-to-use-vh-and-vw-in-webflow?utm_source=google&utm_medium=search&utm_campaign=general-paid-workhorse&utm_term=keyword-targeting&utm_content=dynamic-search-ads-t1&gclid=Cj0KCQjw0PWRBhDKARIsAPKHFGj7OHDDKjzriwKenadeSiEvoiBcRahNwWcuNkoF0COMYYTDaZbpg2UaAts-EALw_wcB
# https://stackoverflow.com/questions/6169666/how-to-resize-an-image-to-fit-in-the-browser-window
# https://pypi.org/project/django-multiselectfield/
# https://docs.djangoproject.com/en/4.0/topics/migrations/
# https://www.reddit.com/r/django/comments/on92qp/noob_no_module_named_multiselectfield/
# https://github.com/microsoft/pylance-release/blob/main/DIAGNOSTIC_SEVERITY_RULES.md#diagnostic-severity-rules
# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# https://medium.com/geekculture/tiny-django-tutorial-bootstrap-cards-25e8dde6f21a
# https://getbootstrap.com/docs/5.0/components/card/
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import RecipePost, RecipeForm
from django.template import loader
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

fav = 0

class HomeView(generic.ListView):
	template_name = 'recipes/home.html'
	def get_queryset(self):
		"""
		Return all recipe posts
		"""
		return RecipePost.objects.all()

#	def get(self, request):
#		return render(request, 'recipes/home.html')
	def post(self, request):
		search = request.POST.get("textinput")
		recipes = RecipePost.objects.filter( 
			Q(title__iexact=search) | 
			Q(intro__iexact=search) | 
			Q(author__iexact=search) |
			Q(cook_time__iexact=search) | 
			Q(servings__iexact=search) 
		)
		print(recipes)
#			results = ""
#			return HttpResponseRedirect('/home/')
		return render(request, 'recipes/home.html', {'recipes':recipes})

class RecipeFeedView(generic.ListView):
	template_name = 'recipes/feed.html'
	context_object_name = 'recipes_list'
	def get_queryset(self):
		return RecipePost.objects.all().order_by('-pub_date')[::1]
	
	def post(self, request):
		search = request.POST.get("textinput")
		recipes = RecipePost.objects.filter( 
			Q(title__icontains=search) | 
			Q(intro__iexact=search) | 
			Q(author__icontains=search) |
			Q(cook_time__iexact=search) | 
			Q(servings__iexact=search) 
		)
		print(recipes)
		return render(request, 'recipes/feed.html', {'recipes':recipes.order_by('-pub_date')[::1]})

def RecipeDetail(request, pk):
	recipe = get_object_or_404(RecipePost, pk=pk)
	fav = False
	if recipe.saved.filter(id=request.user.id).exists():
		fav = True
	return render(request, 'recipes/recipe_detail.html', {'recipe':recipe, 'fav':fav})

def RecipeDetailEdit(request, pk):
	recipe = get_object_or_404(RecipePost, pk=pk)
	return render(request, 'recipes/recipe_edit.html', {'recipe':recipe})

def delete_recipe(request, pk):
	recipe = get_object_or_404(RecipePost, pk=pk)
	if request.user == recipe.user:
		if request.method == 'POST':
			if request.POST.get("del_button"):
				RecipePost.objects.filter(pk=pk).delete()
				return HttpResponseRedirect('/my_posts/')
			if request.POST.get("back"):
				return render(request, 'recipes/recipe_edit.html', {'recipe':recipe})
	return render(request, 'recipes/delete_conf.html', {'recipe':recipe})

def edit_post(request, pk):
	recipe = get_object_or_404(RecipePost, pk=pk)
	if request.method != 'POST':
		form = RecipeForm(instance=recipe)
		return render(request, 'recipes/edit_post.html', {'form':form})
	if request.method == 'POST':
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			recipe.title = form.cleaned_data['title']
			recipe.author = form.cleaned_data['author']
			recipe.intro = form.cleaned_data['intro']
			recipe.cook_time = form.cleaned_data['cook_time']
			recipe.servings = form.cleaned_data['servings']
			if form.cleaned_data['recipe_image'] != 'images/wordofmouth.png':
				recipe.recipe_image = form.cleaned_data['recipe_image']
			recipe.save()
			return render(request, 'recipes/recipe_edit.html', {'recipe':recipe})

def save_new(request, id):
	recipe = get_object_or_404(RecipePost, id=id)
	if recipe.saved.filter(id=request.user.id).exists():
		recipe.saved.remove(request.user)
	else:
		recipe.saved.add(request.user)
		recipe.save()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

def saved_posts(request):
	new = RecipePost.objects.filter(saved=request.user)
	return render(request, 'recipes/saved_posts.html', {'new':new})

def my_posts(request):
	posts = RecipePost.objects.filter(user=request.user)
	return render(request, 'recipes/my_posts.html', {'posts':posts})

class NewPostView(generic.ListView):
	template_name = 'recipes/post.html'
	def get(self, request):
		form = RecipeForm()
		return render(request, 'recipes/post.html', {'form':form})

	def post(self, request):
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			print("VALID")
			newPost = RecipePost()
			newPost.title = form.cleaned_data['title']
			newPost.author = form.cleaned_data['author']
			newPost.intro = form.cleaned_data['intro']
			newPost.ingredients = form.cleaned_data['ingredients']
			newPost.cook_time = form.cleaned_data['cook_time']
			newPost.servings = form.cleaned_data['servings']
			newPost.user = request.user
			newPost.recipe_image = form.cleaned_data['recipe_image']
			newPost.save()
			#RecipePost.upload_image(newPost.recipe_image, newPost.recipe_image.name)
			return HttpResponseRedirect('/feed/')
		else:
			print("NOT VALID")
		return render(request, self.template_name, {'form':form})

def fork_post(request, pk):
	recipe = get_object_or_404(RecipePost, pk=pk)
	#u = recipe.author
	v = recipe.id
	q = recipe.recipe_image
	if request.method != 'POST':
		form = RecipeForm(instance=recipe)
		return render(request, 'recipes/fork_recipe.html', {'form':form, 'recipe':recipe})
	if request.method == 'POST':
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			forked = RecipePost()
			forked.title = form.cleaned_data['title']
			forked.author = request.user.username
			forked.intro = form.cleaned_data['intro']
			forked.ingredients = form.cleaned_data['ingredients']
			forked.cook_time = form.cleaned_data['cook_time']
			forked.servings = form.cleaned_data['servings']
			forked.forked = 1
			forked.forkedid = v
			forked.recipe_image = q
			forked.user = request.user
			forked.save()
			return render(request, 'recipes/recipe_detail.html', {'recipe':forked})
