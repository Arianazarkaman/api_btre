from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='listings'),  # for listing index page
    path('<int:listing_id>/', views.listing, name='listing'),  # add a trailing slash here
    path('search/', views.search, name='search'),  # for search functionality
]
