from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'recipes'

urlpatterns = [
	path('logout/', LogoutView.as_view(), name='logout'),
	path('home/logout/', LogoutView.as_view()),
	path('', views.HomeView.as_view(), name='home'),
	path('home/', views.HomeView.as_view()),
	path('feed/', views.RecipeFeedView.as_view(), name='feed'),
	path('<int:pk>/', views.RecipeDetail, name='recipe_detail'),
	path('saved/<int:id>/', views.save_new, name='save_new'),
	path('saved_posts/', views.saved_posts, name='saved_posts'),
	path('my_posts/', views.my_posts, name='my_posts'),
	path('<int:pk>/edit/', views.RecipeDetailEdit, name='edit'),
	path('<int:pk>/delete/', views.delete_recipe, name='delete'),
	path('<int:pk>/editpost/', views.edit_post, name='editpost'),
	path('<int:pk>/fork/', views.fork_post, name='fork'),
	path('post/', views.NewPostView.as_view(), name='post'),
]